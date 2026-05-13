from pydantic import BaseModel


class WorkflowRequest(BaseModel):
    topic: str


class WorkflowResponse(BaseModel):
    result: str
    status: str = "completed"

