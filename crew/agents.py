from crewai import Agent, LLM
import os

def get_llm():
    return LLM(
        model="azure/gpt-4o",
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

def researcher_agent()-> Agent:
    return Agent(
        role="Researcher Analysis",
        goal="Find accurate and relevant information about {topic}",
        backstory="You are an expert at gathering and synthesizing information.",
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )


def writer_agent() -> Agent:
    return Agent(
        role="Content Writer",
        goal="Write a clear and engaging summary about {topic}",
        backstory="You turn complex research into readable content.",
        verbose=True,
        allow_delegation=False,
        llm=get_llm() 
    )