from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NotificationCreate(BaseModel):
    user_id: int
    title: str = Field(..., max_length=150)
    message: str
    type: str = "SYSTEM"
    metadata_json: Optional[str] = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    metadata_json: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
