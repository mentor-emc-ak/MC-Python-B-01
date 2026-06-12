"""Chat router - conversations and AI messaging."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.models.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.auth_service import get_current_user
from app.services.ai_service import get_ai_response, get_conversation_context


router = APIRouter(prefix="/api/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    content: str = Field(..., min_length=1)
    conversation_id: Optional[int] = None


class ConversationCreate(BaseModel):
    title: str = Field(default="New Chat", min_length=1, max_length=255)


class ConversationUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


# ---- Conversations ----

@router.get("/conversations")
def list_conversations(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


@router.post("/conversations", status_code=201)
def create_conversation(
    data: ConversationCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = Conversation(user_id=user.id, title=data.title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"id": conv.id, "user_id": conv.user_id, "title": conv.title}


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user.id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return {"id": conv.id, "user_id": conv.user_id, "title": conv.title}


@router.patch("/conversations/{conversation_id}")
def rename_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user.id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    conv.title = data.title
    db.commit()
    db.refresh(conv)
    return {"id": conv.id, "user_id": conv.user_id, "title": conv.title}


@router.delete("/conversations/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user.id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    db.delete(conv)
    db.commit()


# ---- Messages ----

@router.get("/conversations/{conversation_id}/messages")
def get_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 50,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user.id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": m.id,
            "conversation_id": m.conversation_id,
            "sender": m.sender,
            "content": m.content,
            "created_at": str(m.created_at),
        }
        for m in msgs
    ]


# ---- Send message + AI reply ----

@router.post("/send")
def send_message(
    data: ChatRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Resolve or create conversation
    if data.conversation_id:
        conv = (
            db.query(Conversation)
            .filter(Conversation.id == data.conversation_id, Conversation.user_id == user.id)
            .first()
        )
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
    else:
        title = data.content[:50] + ("..." if len(data.content) > 50 else "")
        conv = Conversation(user_id=user.id, title=title)
        db.add(conv)
        db.commit()
        db.refresh(conv)

    history = get_conversation_context(db, conv.id)

    user_msg = Message(conversation_id=conv.id, sender="user", content=data.content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    try:
        ai_reply_text = get_ai_response(data.content, conversation_history=history)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"AI error: {e}")

    ai_msg = Message(conversation_id=conv.id, sender="ai", content=ai_reply_text)
    db.add(ai_msg)
    if not history:
        conv.title = data.content[:50] + ("..." if len(data.content) > 50 else "")
    db.commit()
    db.refresh(ai_msg)

    return {
        "message": {
            "id": user_msg.id,
            "conversation_id": user_msg.conversation_id,
            "sender": user_msg.sender,
            "content": user_msg.content,
        },
        "ai_reply": {
            "id": ai_msg.id,
            "conversation_id": ai_msg.conversation_id,
            "sender": ai_msg.sender,
            "content": ai_msg.content,
        },
        "conversation_id": conv.id,
        "conversation_title": conv.title,
    }
