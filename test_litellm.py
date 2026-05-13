import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model="azure/gpt-4o-2",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

response = llm.call(messages=[{"role": "user", "content": "say hello"}])
print("SUCCESS:", response)
