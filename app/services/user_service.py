from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.user import User
from app.models.enums import UserRole

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(
        User.email == email,
        User.is_deleted == False
    ).first()

def get_user_by_google_id(db: Session, google_id: str) -> Optional[User]:
    return db.query(User).filter(
        User.google_id == google_id,
        User.is_deleted == False
    ).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(
        User.id == user_id,
        User.is_deleted == False
    ).first()

def upsert_google_user(
    db: Session, 
    *, 
    google_id: str, 
    email: str, 
    name: Optional[str] = None, 
    picture: Optional[str] = None,
    preferences: Optional[Dict[str, Any]] = None
) -> User:
    user = get_user_by_google_id(db, google_id) or get_user_by_email(db, email)
    if user:
        user.name = name or user.name
        user.picture = picture or user.picture
        if preferences:
            user.preferences = {**user.preferences, **preferences}
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    user = User(
        google_id=google_id,
        email=email,
        name=name,
        picture=picture,
        preferences=preferences or {},
        role=UserRole.USER,
        metadata={}
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_preferences(
    db: Session,
    user_id: str,
    preferences: Dict[str, Any]
) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.preferences = {**user.preferences, **preferences}
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_role(
    db: Session,
    user_id: str,
    role: UserRole
) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.role = role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_metadata(
    db: Session,
    user_id: str,
    metadata: Dict[str, Any]
) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.metadata = {**user.metadata, **metadata}
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def soft_delete_user(db: Session, user_id: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    user.is_deleted = True
    db.add(user)
    db.commit()
    return True
