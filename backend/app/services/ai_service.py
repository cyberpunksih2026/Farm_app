import uuid
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from app.models.ai import AIConversation, AIMessage
from app.models.user import User
from app.ai.ollama import ollama_client
from app.ai.prompts import FARMAPP_AI_SYSTEM_PROMPT
from app.schemas.ai import AIChatRequest, AIChatResponse


class AIService:
    @staticmethod
    def chat(db: Session, chat_req: AIChatRequest, user: Optional[User] = None) -> AIChatResponse:
        conv_id = chat_req.conversation_id or str(uuid.uuid4())

        conv = db.query(AIConversation).filter(AIConversation.conversation_id == conv_id).first()
        if not conv:
            conv = AIConversation(
                conversation_id=conv_id,
                user_id=user.id if user else None,
                title=chat_req.message[:50]
            )
            db.add(conv)
            db.flush()

        # Save user message
        user_msg = AIMessage(
            conversation_id=conv_id,
            role="user",
            content=chat_req.message
        )
        db.add(user_msg)
        db.flush()

        # Retrieve past message history
        past_msgs = db.query(AIMessage).filter(
            AIMessage.conversation_id == conv_id
        ).order_by(AIMessage.created_at.asc()).limit(8).all()

        formatted_history: List[Dict[str, str]] = [
            {"role": m.role, "content": m.content} for m in past_msgs
        ]
        if not formatted_history:
            formatted_history = [{"role": "user", "content": chat_req.message}]

        response_text, is_fallback = ollama_client.chat(
            formatted_history,
            system_prompt=FARMAPP_AI_SYSTEM_PROMPT
        )

        assistant_content = response_text or "I am here to assist with fresh produce recommendations and price breakdowns."

        assistant_msg = AIMessage(
            conversation_id=conv_id,
            role="assistant",
            content=assistant_content,
            tokens_used=len(assistant_content.split())
        )
        db.add(assistant_msg)
        db.commit()

        return AIChatResponse(
            conversation_id=conv_id,
            role="assistant",
            response=assistant_content,
            model_used=ollama_client.model if not is_fallback else "farmapp-heuristic-ai",
            is_fallback=is_fallback
        )
