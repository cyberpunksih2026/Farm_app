from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class AIChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User prompt or question to FarmApp AI")
    conversation_id: Optional[str] = Field(None, description="Session ID for continuous conversation")


class AIMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AIChatResponse(BaseModel):
    conversation_id: str
    role: str = "assistant"
    response: str
    model_used: str
    is_fallback: bool = False
