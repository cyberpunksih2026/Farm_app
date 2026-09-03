from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.schemas.common import APIResponse
from app.services.ai_service import AIService
from app.api.v1.deps import get_optional_current_user

router = APIRouter(prefix="/ai", tags=["FarmApp AI Assistant"])


@router.post("/chat", response_model=APIResponse[AIChatResponse])
def chat_with_ai(
    chat_req: AIChatRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    resp = AIService.chat(db, chat_req, user=current_user)
    return APIResponse(
        success=True,
        message="AI response generated successfully",
        data=resp
    )
