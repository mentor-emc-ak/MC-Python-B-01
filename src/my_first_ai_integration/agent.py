from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[]
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Explain LangChain in one sentence."
        }
    ]
})

print(result)
