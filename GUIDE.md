# CrewAI + FastAPI Agentic Workflow — Implementation Guide

## What You're Building

A FastAPI server that exposes endpoints to trigger **CrewAI multi-agent workflows**.
Clients hit the API → FastAPI kicks off a Crew → agents collaborate → result returned.

---

## Step 1: Project Setup

### Folder structure you'll create
```
crewai-fastapi/
├── main.py              # FastAPI app entry point
├── crew/
│   ├── __init__.py
│   ├── agents.py        # Agent definitions
│   ├── tasks.py         # Task definitions
│   └── crew.py          # Crew assembly + kickoff
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic request/response models
├── routers/
│   ├── __init__.py
│   └── workflow.py      # API route handlers
├── .env                 # API keys
└── requirements.txt
```

### Install dependencies
```bash
pip install crewai fastapi uvicorn python-dotenv
```

`requirements.txt`:
```
crewai
crewai-tools
fastapi
uvicorn[standard]
python-dotenv
```

---

## Step 2: Environment Variables

`.env`:
```
OPENAI_API_KEY=sk-...
```

CrewAI uses OpenAI by default. You can swap to any LLM later.

---

## Step 3: Pydantic Schemas (`models/schemas.py`)

Define what the API receives and returns.

```python
from pydantic import BaseModel

class WorkflowRequest(BaseModel):
    topic: str                    # input from the user

class WorkflowResponse(BaseModel):
    result: str                   # final crew output
    status: str = "completed"
```

**Key concept:** FastAPI validates incoming JSON against `WorkflowRequest` automatically.

---

## Step 4: Define Agents (`crew/agents.py`)

Each agent has a **role**, **goal**, and **backstory**. These shape how the LLM behaves.

```python
from crewai import Agent

def researcher_agent() -> Agent:
    return Agent(
        role="Research Analyst",
        goal="Find accurate and relevant information about {topic}",
        backstory="You are an expert at gathering and synthesizing information.",
        verbose=True,
        allow_delegation=False,   # this agent won't hand off to others
    )

def writer_agent() -> Agent:
    return Agent(
        role="Content Writer",
        goal="Write a clear and engaging summary about {topic}",
        backstory="You turn complex research into readable content.",
        verbose=True,
        allow_delegation=False,
    )
```

**Key concepts:**
- `verbose=True` — logs agent thinking to console (great for debugging)
- `allow_delegation=True` — lets an agent assign subtasks to other agents
- `{topic}` placeholders get filled at crew kickoff time

---

## Step 5: Define Tasks (`crew/tasks.py`)

Tasks are the **units of work** assigned to agents. Each task needs a description, expected output, and an assigned agent.

```python
from crewai import Task
from crew.agents import researcher_agent, writer_agent

def research_task(agent) -> Task:
    return Task(
        description=(
            "Research the topic: {topic}. "
            "Gather key facts, trends, and insights."
        ),
        expected_output="A bullet-point summary of key findings.",
        agent=agent,
    )

def writing_task(agent, context_tasks: list) -> Task:
    return Task(
        description=(
            "Using the research provided, write a 3-paragraph summary about {topic}."
        ),
        expected_output="A polished 3-paragraph article.",
        agent=agent,
        context=context_tasks,   # this task waits for research_task output
    )
```

**Key concept:** `context=` creates a dependency — the writing task receives the research task's output as input.

---

## Step 6: Assemble the Crew (`crew/crew.py`)

The Crew wires agents and tasks together and defines how they collaborate.

```python
from crewai import Crew, Process
from crew.agents import researcher_agent, writer_agent
from crew.tasks import research_task, writing_task

def build_crew() -> Crew:
    researcher = researcher_agent()
    writer = writer_agent()

    task1 = research_task(researcher)
    task2 = writing_task(writer, context_tasks=[task1])

    return Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        process=Process.sequential,   # tasks run one after another
        verbose=True,
    )
```

**Key concepts:**
- `Process.sequential` — tasks execute in order (task1 → task2)
- `Process.hierarchical` — a manager agent delegates tasks dynamically (needs a manager LLM)

---

## Step 7: API Routes (`routers/workflow.py`)

```python
from fastapi import APIRouter, HTTPException
from models.schemas import WorkflowRequest, WorkflowResponse
from crew.crew import build_crew

router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.post("/run", response_model=WorkflowResponse)
async def run_workflow(request: WorkflowRequest):
    try:
        crew = build_crew()
        result = crew.kickoff(inputs={"topic": request.topic})
        return WorkflowResponse(result=str(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Key concept:** `crew.kickoff(inputs={...})` fills in all `{topic}` placeholders across agents and tasks.

---

## Step 8: FastAPI App Entry Point (`main.py`)

```python
from fastapi import FastAPI
from dotenv import load_dotenv
from routers.workflow import router as workflow_router

load_dotenv()

app = FastAPI(
    title="CrewAI Agentic Workflow API",
    version="1.0.0",
)

app.include_router(workflow_router)

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## Step 9: Run the Server

```bash
uvicorn main:app --reload
```

Test it:
```bash
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing trends in 2025"}'
```

Or open the auto-generated docs: `http://localhost:8000/docs`

---

## Step 10: Add Tools to Agents (Optional but Powerful)

CrewAI agents can use tools like web search:

```python
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()   # needs SERPER_API_KEY in .env

researcher = Agent(
    role="Research Analyst",
    goal="...",
    backstory="...",
    tools=[search_tool],        # agent will call this tool when needed
)
```

Other useful tools: `ScrapeWebsiteTool`, `FileReadTool`, `CSVSearchTool`, `CodeInterpreterTool`

---

## Step 11: Make it Async (Production Pattern)

Long-running crews shouldn't block the HTTP response. Use background tasks + polling:

```python
import asyncio
from fastapi import BackgroundTasks
from uuid import uuid4

jobs = {}   # in production, use Redis or a DB

@router.post("/run/async")
async def run_async(request: WorkflowRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())
    jobs[job_id] = {"status": "running", "result": None}
    background_tasks.add_task(run_crew_job, job_id, request.topic)
    return {"job_id": job_id}

@router.get("/status/{job_id}")
def get_status(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})

def run_crew_job(job_id: str, topic: str):
    crew = build_crew()
    result = crew.kickoff(inputs={"topic": topic})
    jobs[job_id] = {"status": "completed", "result": str(result)}
```

---

## Core Concepts Summary

| Concept | What it does |
|---|---|
| `Agent` | An LLM persona with a role, goal, and backstory |
| `Task` | A unit of work assigned to an agent |
| `Crew` | Orchestrates agents + tasks; runs the workflow |
| `Process.sequential` | Tasks run one after another in order |
| `Process.hierarchical` | Manager agent delegates tasks dynamically |
| `context=` on a Task | Creates a data dependency between tasks |
| `tools=` on an Agent | Gives an agent callable capabilities (search, scrape, etc.) |
| `crew.kickoff(inputs={})` | Starts the workflow; fills `{placeholders}` in all prompts |

---

## Build Order Checklist

- [ ] Install deps, set up `.env`
- [ ] Write Pydantic schemas (`models/schemas.py`)
- [ ] Define agents (`crew/agents.py`)
- [ ] Define tasks with `context=` dependencies (`crew/tasks.py`)
- [ ] Assemble crew with `Process.sequential` (`crew/crew.py`)
- [ ] Write FastAPI route that calls `crew.kickoff()` (`routers/workflow.py`)
- [ ] Wire up `main.py`, run with `uvicorn`
- [ ] Test via `/docs` or `curl`
- [ ] (Optional) Add tools, async job pattern, persistent job store
