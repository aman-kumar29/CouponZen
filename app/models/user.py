from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, JSON

class User(SQLModel, table=True):
    __tablename__ = "users"
    # indexes/uniques via __table_args__ handled by Field(unique=True, index=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)

    # Google OIDC identity (no passwords)
    email: str = Field(index=True, unique=True)
    google_sub: str = Field(index=True, unique=True)  # Google's subject
    name: Optional[str] = None
    picture: Optional[str] = None
    email_verified: bool = Field(default=False)

    # Optional phone (for SMS reminders later)
    phone: Optional[str] = Field(default=None, unique=True)

    # User preferences and settings
    preferences: Dict = Field(default={}, sa_column=Column(JSON))  # Notification settings, timezone, etc.
    role: str = Field(default="user", index=True)  # user, admin, etc.
    status: str = Field(default="active", index=True)  # active, suspended, deleted

    # Audit fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None  # For soft delete
    version: int = Field(default=1)  # For optimistic locking
