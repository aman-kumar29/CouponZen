from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid

class AppUser(SQLModel, table=True):
    __tablename__ = "app_users"
    # indexes/uniques via __table_args__ handled by Field(unique=True, index=True)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    # Google OIDC identity (no passwords)
    email: str = Field(index=True, unique=True, nullable=False)
    google_sub: str = Field(index=True, unique=True, nullable=False)  # Google's subject
    name: Optional[str] = None
    picture: Optional[str] = None
    email_verified: bool = Field(default=False, nullable=False)

    # Optional phone (for SMS reminders later)
    phone: Optional[str] = Field(default=None, unique=True)

    # JSON for notification prefs / quiet hours
    notification_prefs: dict | None = Field(default=None, sa_column_kwargs={"nullable": True})

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
