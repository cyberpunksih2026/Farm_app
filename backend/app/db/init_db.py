from datetime import datetime, timezone
import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine, SessionLocal
# Import all SQLAlchemy models to register them on Base.metadata before create_all
import app.models  
from app.models.user import User, UserRole
from app.models.setting import Setting
from app.core.security import get_password_hash

logger = logging.getLogger("attendance.init_db")


def init_db(db: Optional[Session] = None) -> None:
    """
    Ensure all database tables exist and seed initial administrator account (Rajavel)
    and configurable system settings without destroying existing data.
    """
    logger.info("Verifying database schema and registering SQLAlchemy models...")
    
    # 1. Ensure all models are registered and create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified.")

    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # 2. Check or create default user 'Admin'
        admin_user = db.query(User).filter(
            (User.username == "Admin") | 
            (User.email == "ishanrajavelu75@gmail.com") |
            (User.email == "ishanrajavelu75@gmail.com")
        ).first()
        
        if not admin_user:
            admin_user = User(
                username="Admin",
                full_name="Admin",
                email="ishanrajavelu75@gmail.com",
                phone="8110814178",
                password_hash=get_password_hash("Admin@123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_email_verified=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.add(admin_user)
            logger.info("Created default user account (username: Admin, password: Admin@123)")
        else:
            admin_user.username = "Admin"
            admin_user.email = "ishanrajavelu75@gmail.com"
            admin_user.phone = "8110814178"
            admin_user.role = UserRole.ADMIN
            admin_user.is_active = True
            admin_user.password_hash = get_password_hash("Admin@123")

        # 3. Check or create default demo Customer account
        demo_customer = db.query(User).filter(
            (User.username == "demo_customer") | 
            (User.email == "customer@farmapp.in")
        ).first()

        if not demo_customer:
            demo_customer = User(
                username="demo_customer",
                full_name="Priya Sharma",
                email="customer@farmapp.in",
                phone="9876543210",
                password_hash=get_password_hash("Customer@123"),
                role=UserRole.CUSTOMER,
                is_active=True,
                is_email_verified=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.add(demo_customer)
            logger.info("Created demo customer account (email: customer@farmapp.in, password: Customer@123)")
        else:
            demo_customer.role = UserRole.CUSTOMER
            demo_customer.is_active = True
            demo_customer.password_hash = get_password_hash("Customer@123")

        # 4. Seed Configurable System Settings if missing
        default_settings = [
            ("company_name", "FarmApp", "Company or organization display name"),
            ("admin_notification_email", "ishanrajavelu75@gmail", "Primary admin email for alerts")
        ]

        for key, value, desc in default_settings:
            setting = db.query(Setting).filter(Setting.key == key).first()
            if not setting:
                db.add(Setting(key=key, value=value, description=desc))

        db.commit()
        logger.info("Database startup initialization completed successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during database initialization: {e}", exc_info=True)
        raise
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    init_db()
