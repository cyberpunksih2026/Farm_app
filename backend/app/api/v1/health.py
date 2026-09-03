import logging
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.ai.ollama import ollama_client
from app.services.email_service import EmailService

logger = logging.getLogger("farmapp.health")
router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "dialect": db.bind.dialect.name if db.bind else "unknown"
        }
    except Exception as e:
        logger.error(f"Health DB check error: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@router.get("/health/ai")
def health_ai():
    is_online = ollama_client.check_health()
    return {
        "status": "healthy" if is_online else "fallback_mode",
        "ollama_connected": is_online,
        "model": ollama_client.model,
        "base_url": settings.OLLAMA_BASE_URL
    }


@router.get("/health/system")
def health_system(db: Session = Depends(get_db)):
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    ai_ok = ollama_client.check_health()
    smtp_info = EmailService.get_smtp_status()

    return {
        "status": "healthy" if db_ok else "degraded",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "components": {
            "database": "connected" if db_ok else "disconnected",
            "ai_inference": "ollama_ready" if ai_ok else "heuristic_fallback_ready",
            "smtp_email": "configured" if smtp_info["is_configured"] else "dev_mock_mode"
        }
    }
