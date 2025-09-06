from sqlmodel import SQLModel, Field
from sqlalchemy import Index, UniqueConstraint
from datetime import datetime, timezone
from typing import Optional
import uuid
class RefreshToken(SQLModel, table=True):
    __tablename__ = "refreshtoken"
    __table_args__ = (
        Index("ix_refreshtoken_user_id", "user_id"),
        UniqueConstraint("token", name="uq_refreshtoken_token"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)  # SERIAL
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    token: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    revoked: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)