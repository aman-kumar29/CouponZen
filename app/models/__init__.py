# Importing here ensures SQLModel metadata sees all tables
from .user import AppUser
from .coupon import AppCoupon
from .inbound_item import AppInboundItem
from .reminder import AppReminder
from .enums import CouponSource, ReminderChannel, ItemStatus  # re-export for convenience

__all__ = [
    "AppUser", "AppCoupon", "AppInboundItem", "AppReminder",
    "CouponSource", "ReminderChannel", "ItemStatus"
]
