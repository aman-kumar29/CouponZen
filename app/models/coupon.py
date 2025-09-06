from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint, Index, Column, JSON, ARRAY
from typing import Optional, Dict, List
from datetime import datetime, timezone
import uuid
from .enums import CouponSource

class Coupon(SQLModel, table=True):
    """
    Coupon model representing discount coupons in the system.
    Single-column indexes are defined directly on fields using index=True.
    Compound indexes are defined in __table_args__ as they span multiple columns.
    """
    __tablename__ = "coupons"
    
    # Define compound indexes and constraints that span multiple columns
    __table_args__ = (
        # Index for finding user's coupons by expiration
        Index('idx_coupons_user_expires', 'user_id', 'expires_at'),
        # Index for public coupon discovery
        Index('idx_coupons_visibility_status', 'visibility', 'processing_status'),
        # Ensure no duplicate coupons
        UniqueConstraint('dedupe_hash', name='uq_coupons_dedupe')
    )

    # Primary keys and relationships
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    inbound_item_id: Optional[str] = Field(default=None, foreign_key="inbound_items.id")
    
    # Brand and Categories
    brand: str = Field(index=True)
    brand_id: Optional[str] = None  # future FK
    categories: List[str] = Field(default=[], sa_column=Column(ARRAY(str)))  # For categorization
    tags: List[str] = Field(default=[], sa_column=Column(ARRAY(str)))  # For flexible tagging

    # What users see
    title: str
    description: Optional[str] = None
    code: Optional[str] = Field(default=None, index=True)
    source: CouponSource = Field(default=CouponSource.MANUAL)
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
    terms: Dict = Field(default={}, sa_column=Column(JSON))
    metadata: Dict = Field(default={}, sa_column=Column(JSON))  # For extensible properties
    is_redeemed: bool = Field(default=False)
    redeemed_at: Optional[datetime] = None
    is_archived: bool = Field(default=False)
    
    # Validation and processing
    validation_rules: Dict = Field(default={}, sa_column=Column(JSON))  # Custom validation rules
    processing_status: str = Field(default="active")  # active, expired, invalid
    error_message: Optional[str] = None

    # System
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None  # For soft delete
    dedupe_hash: Optional[str] = Field(default=None, unique=True)
    version: int = Field(default=1)

    # Public sharing (future sprints—harmless now)
    visibility: Optional[str] = Field(default="PRIVATE")  # PRIVATE | PUBLIC | UNLISTED
    share_slug: Optional[str] = Field(default=None, unique=True)
    is_public_only: bool = Field(default=False)
    max_claims: Optional[int] = Field(default=0)  # 0 = unlimited
    claims_used: int = Field(default=0, nullable=False)
