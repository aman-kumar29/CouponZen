from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.security import create_jwt_token
from app.models.refresh_token import RefreshToken

def issue_access_token(user_id: int) -> str:
    try:
        logger.info(f"Issuing access token for user_id: {user_id}")
        token = create_jwt_token(str(user_id), expires_minutes=180) # 3 hours
        logger.info("Access token issued successfully.")
        return token
    except Exception as e:
        logger.error(f"Error issuing access token: {e}")
        raise

def issue_refresh_token(db: Session, user_id: int) -> str:
    try:
        logger.info(f"Issuing refresh token for user_id: {user_id}")
        token = create_jwt_token(str(user_id), expires_minutes=60*24*7)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        db.add(RefreshToken(user_id=user_id, token=token, expires_at=expires_at, revoked=False))
        db.commit()
        logger.info("Refresh token issued and saved to database.")
        return token
    except Exception as e:
        logger.error(f"Error issuing refresh token: {e}")
        raise
def validate_refresh_token(db: Session, token: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.token == token, RefreshToken.revoked == False).first()
