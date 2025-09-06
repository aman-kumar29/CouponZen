from sqlmodel import SQLModel, Field
from sqlalchemy import Index
from typing import Optional
from datetime import datetime, timezone
import uuid
from .enums import ReminderChannel

class AppReminder(SQLModel, table=True):
    __tablename__ = "app_reminders"
    __table_args__ = (
        Index("idx_app_reminders_user_schedule", "user_id", "scheduled_at"),
        Index("idx_app_reminders_coupon", "coupon_id"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: str = Field(foreign_key="app_users.id", index=True)
    coupon_id: str = Field(foreign_key="app_coupons.id", index=True)
    channel: ReminderChannel = Field(default=ReminderChannel.PUSH)
    scheduled_at: datetime = Field(index=True)
    sent_at: Optional[datetime] = None
    
    cancelled_at: Optional[datetime] = None
    retry_count: int = Field(default=0, nullable=False)

    notification_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
