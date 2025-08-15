from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_google_id(db: Session, google_id: str) -> User | None:
    return db.query(User).filter(User.google_id == google_id).first()

def upsert_google_user(db: Session, *, google_id: str, email: str, name: str | None, picture: str | None) -> User:
    user = get_user_by_google_id(db, google_id) or get_user_by_email(db, email)
    if user:
        user.name = name or user.name
        user.picture = picture or user.picture
        db.add(user); db.commit(); db.refresh(user)
        return user
    user = User(google_id=google_id, email=email, name=name, picture=picture)
    db.add(user); db.commit(); db.refresh(user)
    return user
