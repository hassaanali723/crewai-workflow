import asyncio
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from models.schemas import WorkflowRequest, WorkflowResponse
from crew.crew import build_crew

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("/run", response_model=WorkflowResponse)
async def run_workflow(request: WorkflowRequest) -> WorkflowResponse:
    try:
        crew = build_crew()
        result = crew.kickoff(inputs={"topic": request.topic})
        return WorkflowResponse(result=str(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run/stream")
async def run_workflow_stream(request: WorkflowRequest):
    async def event_stream():
        try:
            yield "data: {\"status\": \"started\", \"message\": \"Crew is starting...\"}\n\n"

            loop = asyncio.get_event_loop()
            crew = build_crew()

            result = await loop.run_in_executor(
                None,
                lambda: crew.kickoff(inputs={"topic": request.topic})
            )

            yield f"data: {{\"status\": \"completed\", \"result\": {repr(str(result))}}}\n\n"

        except Exception as e:
            yield f"data: {{\"status\": \"error\", \"message\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
