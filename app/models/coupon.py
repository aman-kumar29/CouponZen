from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint, Index
from typing import Optional
from datetime import datetime, timezone
import uuid
from .enums import CouponSource

class AppCoupon(SQLModel, table=True):
    __tablename__ = "app_coupons"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: str = Field(foreign_key="app_users.id", index=True)
    inbound_item_id: Optional[str] = Field(default=None, foreign_key="app_inbound_items.id")
    # Brand
    brand: str = Field(nullable=False)
    brand_id: Optional[uuid.UUID] = None  # future FK

    # What users see
    title: str = Field(nullable=False)
    description: Optional[str] = None
    code: Optional[str] = None
    source: CouponSource = Field(default=CouponSource.MANUAL, nullable=False)
    url: Optional[str] = None
    image_uri: Optional[str] = None

    # Timing
    issued_at: Optional[datetime] = None
    expires_at: datetime = Field(nullable=False)
    reminder_threshold: int = Field(default=3)  # days before expiry

    # Value
    estimated_value: Optional[float] = None
    currency: str = Field(default="INR")
    discount_percent: Optional[int] = None

    # Metadata / state
    terms: dict | None = Field(default=None, sa_column_kwargs={"nullable": True})
    is_redeemed: bool = Field(default=False, nullable=False)
    redeemed_at: Optional[datetime] = None
    is_archived: bool = Field(default=False, nullable=False)

    # System
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    dedupe_hash: Optional[str] = Field(default=None, unique=True)
    version: int = Field(default=1, nullable=False)

    # Public sharing (future sprints—harmless now)
    visibility: Optional[str] = Field(default="PRIVATE")  # PRIVATE | PUBLIC | UNLISTED
    share_slug: Optional[str] = Field(default=None, unique=True)
    is_public_only: bool = Field(default=False)
    max_claims: Optional[int] = Field(default=0)  # 0 = unlimited
    claims_used: int = Field(default=0, nullable=False)
