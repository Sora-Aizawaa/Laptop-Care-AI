from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # user | technician | admin
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
