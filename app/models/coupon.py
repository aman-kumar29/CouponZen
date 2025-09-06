from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint, Index, Column, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from typing import Optional, Dict, List
from datetime import datetime, timezone
import uuid
from .enums import CouponSource

class Coupon(SQLModel, table=True):
    __tablename__ = "coupons"
    __table_args__ = (
        Index("idx_coupons_user_expires", "user_id", "expires_at"),
        Index("idx_coupons_visibility_status", "visibility", "processing_status"),
        UniqueConstraint("dedupe_hash", name="uq_coupons_dedupe"),
    )

    # IDs
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    inbound_item_id: Optional[uuid.UUID] = Field(default=None, foreign_key="inbound_items.id")

    # Brand & categories/tags
    brand: str = Field(index=True, nullable=False)
    brand_id: Optional[str] = None
    categories: List[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String()), nullable=False),
    )
    tags: List[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String()), nullable=False),
    )

    # Visible info
    title: str
    description: Optional[str] = None
    code: Optional[str] = Field(default=None, index=True)
    source: CouponSource = Field(default=CouponSource.MANUAL)
    url: Optional[str] = None
    image_uri: Optional[str] = None

    # Timing
    issued_at: Optional[datetime] = None
    expires_at: datetime = Field(nullable=False)
    reminder_threshold: int = Field(default=3)

    # Value
    estimated_value: Optional[float] = None
    currency: str = Field(default="INR")
    discount_percent: Optional[int] = None

    # Metadata / state
    terms: Dict = Field(default_factory=dict, sa_column=Column(JSONB))
    meta_info: Dict = Field(default_factory=dict, sa_column=Column(JSONB))
    is_redeemed: bool = Field(default=False)
    redeemed_at: Optional[datetime] = None
    is_archived: bool = Field(default=False)

    validation_rules: Dict = Field(default_factory=dict, sa_column=Column(JSONB))
    processing_status: str = Field(default="active")  # active | expired | invalid
    error_message: Optional[str] = None

    # System
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None
    dedupe_hash: Optional[str] = Field(default=None, unique=True)
    version: int = Field(default=1)

    # Sharing
    visibility: Optional[str] = Field(default="PRIVATE")  # PRIVATE | PUBLIC | UNLISTED
    share_slug: Optional[str] = Field(default=None, unique=True)
    is_public_only: bool = Field(default=False)
    max_claims: Optional[int] = Field(default=0)
    claims_used: int = Field(default=0, nullable=False)
