from enum import Enum

class CouponSource(str, Enum):
    SHARE_TEXT = "SHARE_TEXT"
    EMAIL = "EMAIL"
    SMS = "SMS"
    OCR = "OCR"
    MANUAL = "MANUAL"
    API = "API"
    PARTNER = "PARTNER"

class CouponStatus(str, Enum):
    ACTIVE = "ACTIVE"
    USED = "USED"
    EXPIRED = "EXPIRED"
    INVALID = "INVALID"
    ARCHIVED = "ARCHIVED"

class CouponVisibility(str, Enum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"
    UNLISTED = "UNLISTED"

class ReminderChannel(str, Enum):
    PUSH = "PUSH"
    EMAIL = "EMAIL"
    SMS = "SMS"

class ItemStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    PARSED = "PARSED"
    FAILED = "FAILED"
    NEEDS_REVIEW = "NEEDS_REVIEW"

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    PARTNER = "PARTNER"
