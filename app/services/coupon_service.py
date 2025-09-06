from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.coupon import Coupon
from app.models.enums import CouponStatus, CouponVisibility

def create_coupon(
    db: Session,
    *,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    expiry_date: Optional[str] = None,
    visibility: CouponVisibility = CouponVisibility.PRIVATE,
    meta_info: Optional[dict] = None,
) -> Coupon:
    coupon = Coupon(
        user_id=user_id,
        title=title,
        description=description,
        expiry_date=expiry_date,
        visibility=visibility,
        meta_info=meta_info or {},
        status=CouponStatus.ACTIVE
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

def get_coupon(db: Session, coupon_id: str) -> Optional[Coupon]:
    return db.query(Coupon).filter(
        Coupon.id == coupon_id,
        Coupon.is_deleted == False
    ).first()

def get_user_coupons(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    status: Optional[CouponStatus] = None
) -> List[Coupon]:
    query = db.query(Coupon).filter(
        Coupon.user_id == user_id,
        Coupon.is_deleted == False
    )
    if status:
        query = query.filter(Coupon.status == status)
    return query.offset(skip).limit(limit).all()

def update_coupon(
    db: Session,
    *,
    coupon_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    expiry_date: Optional[str] = None,
    visibility: Optional[CouponVisibility] = None,
    status: Optional[CouponStatus] = None,
    meta_info: Optional[dict] = None
) -> Optional[Coupon]:
    coupon = get_coupon(db, coupon_id)
    if not coupon:
        return None
    
    if title is not None:
        coupon.title = title
    if description is not None:
        coupon.description = description
    if expiry_date is not None:
        coupon.expiry_date = expiry_date
    if visibility is not None:
        coupon.visibility = visibility
    if status is not None:
        coupon.status = status
    if meta_info is not None:
        coupon.meta_info = {**coupon.meta_info, **meta_info}
    
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

def delete_coupon(db: Session, coupon_id: str) -> bool:
    coupon = get_coupon(db, coupon_id)
    if not coupon:
        return False
    
    coupon.is_deleted = True
    db.add(coupon)
    db.commit()
    return True
