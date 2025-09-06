from enum import Enum

class CouponSource(str, Enum):
    SHARE_TEXT = "SHARE_TEXT"
    EMAIL = "EMAIL"
    SMS = "SMS"
    OCR = "OCR"
    MANUAL = "MANUAL"
    API = "API"
    PARTNER = "PARTNER"

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
