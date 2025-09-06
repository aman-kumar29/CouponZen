from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid

class AppUser(SQLModel, table=True):
    __tablename__ = "app_users"
    # indexes/uniques via __table_args__ handled by Field(unique=True, index=True)

    id: str = Field(default_factory=str(uuid.uuid4()), primary_key=True, index=True)

    # Google OIDC identity (no passwords)
    email: str = Field(index=True, unique=True)
    google_sub: str = Field(index=True, unique=True)  # Google's subject
    name: Optional[str] = None
    picture: Optional[str] = None
    email_verified: bool = Field(default=False)

    # Optional phone (for SMS reminders later)
    phone: Optional[str] = Field(default=None, unique=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
