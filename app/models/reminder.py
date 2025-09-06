from sqlmodel import SQLModel, Field
from sqlalchemy import Index, Column, JSON
from typing import Optional, Dict
from datetime import datetime, timezone
import uuid
from .enums import ReminderChannel

class Reminder(SQLModel, table=True):
    __tablename__ = "reminders"
    __table_args__ = (
        Index("idx_reminders_user_schedule", "user_id", "scheduled_at"),
        Index("idx_reminders_coupon", "coupon_id"),
        Index("idx_reminders_status", "status"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    coupon_id: uuid.UUID = Field(foreign_key="coupons.id", index=True)
    
    # Notification details
    channel: ReminderChannel = Field(default=ReminderChannel.PUSH)
    scheduled_at: datetime = Field(index=True)
    sent_at: Optional[datetime] = None
    
    # Enhanced reminder features
    message: Optional[str] = None  # Custom reminder message
    status: str = Field(default="scheduled", index=True)  # scheduled, sent, failed, cancelled
    preferences: Dict = Field(default={}, sa_column=Column(JSON))  # Channel-specific preferences
    
    cancelled_at: Optional[datetime] = None
    retry_count: int = Field(default=0, nullable=False)

    notification_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
