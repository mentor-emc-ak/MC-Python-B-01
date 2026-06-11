from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

response = model.invoke("What is LangChain?")
print(response.content)
