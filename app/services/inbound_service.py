from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.inbound_item import InboundItem
from app.models.enums import InboundItemStatus, InboundItemType

def create_inbound_item(
    db: Session,
    *,
    user_id: str,
    content: str,
    item_type: InboundItemType,
    metadata: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None
) -> InboundItem:
    item = InboundItem(
        user_id=user_id,
        content=content,
        item_type=item_type,
        status=InboundItemStatus.PENDING,
        metadata=metadata or {},
        source=source
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_inbound_item(db: Session, item_id: str) -> Optional[InboundItem]:
    return db.query(InboundItem).filter(
        InboundItem.id == item_id,
        InboundItem.is_deleted == False
    ).first()

def get_user_inbound_items(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    status: Optional[InboundItemStatus] = None,
    item_type: Optional[InboundItemType] = None
) -> List[InboundItem]:
    query = db.query(InboundItem).filter(
        InboundItem.user_id == user_id,
        InboundItem.is_deleted == False
    )
    
    if status:
        query = query.filter(InboundItem.status == status)
    if item_type:
        query = query.filter(InboundItem.item_type == item_type)
    
    return query.offset(skip).limit(limit).all()

def update_inbound_item_status(
    db: Session,
    item_id: str,
    status: InboundItemStatus,
    error_message: Optional[str] = None
) -> Optional[InboundItem]:
    item = get_inbound_item(db, item_id)
    if not item:
        return None
    
    item.status = status
    if error_message:
        item.error_message = error_message
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def update_inbound_item_info(
    db: Session,
    item_id: str,
    processing_info: Dict[str, Any]
) -> Optional[InboundItem]:
    item = get_inbound_item(db, item_id)
    if not item:
        return None
    
    item.processing_info = {**item.processing_info, **processing_info}
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_inbound_item(db: Session, item_id: str) -> bool:
    item = get_inbound_item(db, item_id)
    if not item:
        return False
    
    item.is_deleted = True
    db.add(item)
    db.commit()
    return True

def get_pending_inbound_items(
    db: Session,
    limit: int = 100,
    item_type: Optional[InboundItemType] = None
) -> List[InboundItem]:
    query = db.query(InboundItem).filter(
        InboundItem.status == InboundItemStatus.PENDING,
        InboundItem.is_deleted == False
    )
    
    if item_type:
        query = query.filter(InboundItem.item_type == item_type)
    
    return query.limit(limit).all()
