from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.reminder import Reminder
from datetime import datetime

def create_reminder(
    db: Session,
    *,
    user_id: str,
    coupon_id: str,
    reminder_date: datetime,
    custom_message: Optional[str] = None,
    metadata: Optional[dict] = None
) -> Reminder:
    reminder = Reminder(
        user_id=user_id,
        coupon_id=coupon_id,
        reminder_date=reminder_date,
        custom_message=custom_message,
        metadata=metadata or {},
        is_sent=False
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_reminder(db: Session, reminder_id: str) -> Optional[Reminder]:
    return db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.is_deleted == False
    ).first()

def get_user_reminders(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    include_sent: bool = False
) -> List[Reminder]:
    query = db.query(Reminder).filter(
        Reminder.user_id == user_id,
        Reminder.is_deleted == False
    )
    if not include_sent:
        query = query.filter(Reminder.is_sent == False)
    return query.offset(skip).limit(limit).all()

def get_pending_reminders(
    db: Session,
    current_time: datetime,
    limit: int = 100
) -> List[Reminder]:
    return db.query(Reminder).filter(
        Reminder.reminder_date <= current_time,
        Reminder.is_sent == False,
        Reminder.is_deleted == False
    ).limit(limit).all()

def mark_reminder_sent(db: Session, reminder_id: str) -> bool:
    reminder = get_reminder(db, reminder_id)
    if not reminder:
        return False
    
    reminder.is_sent = True
    reminder.sent_at = datetime.utcnow()
    db.add(reminder)
    db.commit()
    return True

def update_reminder(
    db: Session,
    *,
    reminder_id: str,
    reminder_date: Optional[datetime] = None,
    custom_message: Optional[str] = None,
    metadata: Optional[dict] = None
) -> Optional[Reminder]:
    reminder = get_reminder(db, reminder_id)
    if not reminder:
        return None
    
    if reminder_date is not None:
        reminder.reminder_date = reminder_date
    if custom_message is not None:
        reminder.custom_message = custom_message
    if metadata is not None:
        reminder.metadata = {**reminder.metadata, **metadata}
    
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def delete_reminder(db: Session, reminder_id: str) -> bool:
    reminder = get_reminder(db, reminder_id)
    if not reminder:
        return False
    
    reminder.is_deleted = True
    db.add(reminder)
    db.commit()
    return True
