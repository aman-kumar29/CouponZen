from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class RefreshToken(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="app_users.id", index=True)
    token: str = Field(unique=True, index=True)
    expires_at: datetime = Field()
    revoked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))