from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint, Index, Column, JSON
from typing import Optional, Dict
from datetime import datetime, timezone
import uuid
from .enums import CouponSource, ItemStatus

class InboundItem(SQLModel, table=True):
    __tablename__ = "inbound_items"
    __table_args__ = (
        UniqueConstraint("hash", name="uq_inbound_hash"),
        Index("idx_inbound_user_status", "user_id", "status"),
        Index("idx_inbound_pipeline", "status", "received_at"),
        Index("idx_inbound_batch", "batch_id"),
    )

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    source: CouponSource = Field()
    raw_text: Optional[str] = None
    raw_url: Optional[str] = None
    media_uri: Optional[str] = None  # screenshot path
    
    # Batch processing support
    batch_id: Optional[str] = Field(default=None, index=True)
    processing_metadata: Dict = Field(default={}, sa_column=Column(JSON))  # For storing processing details

    status: ItemStatus = Field(default=ItemStatus.RECEIVED, nullable=False)
    error_message: Optional[str] = None

    hash: str = Field(unique=True, nullable=False, index=True)
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    processed_at: Optional[datetime] = None
    parsed_coupon_id: Optional[uuid.UUID] = Field(default=None, foreign_key="coupons.id")
