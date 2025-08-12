from jose import jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM

def create_jwt_token(email: str, expires_minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
