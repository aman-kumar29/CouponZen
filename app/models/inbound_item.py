from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint, Index
from typing import Optional
from datetime import datetime, timezone
import uuid
from .enums import CouponSource, ItemStatus

class AppInboundItem(SQLModel, table=True):
    __tablename__ = "app_inbound_items"
    __table_args__ = (
        UniqueConstraint("hash", name="uq_app_inbound_hash"),
        Index("idx_inbound_user_status", "user_id", "status"),
        Index("idx_inbound_pipeline", "status", "received_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: str = Field(foreign_key="app_users.id", index=True)
    source: CouponSource = Field()
    raw_text: Optional[str] = None
    raw_url: Optional[str] = None
    media_uri: Optional[str] = None  # screenshot path

    status: ItemStatus = Field(default=ItemStatus.RECEIVED, nullable=False)
    error_message: Optional[str] = None

    hash: str = Field(unique=True, nullable=False, index=True)
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    processed_at: Optional[datetime] = None
    parsed_coupon_id: Optional[uuid.UUID] = Field(default=None, foreign_key="app_coupons.id")
