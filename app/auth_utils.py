from jose import jwt
from datetime import datetime, timedelta

JWT_ALGORITHM = "HS256"

def create_jwt_token(email: str, expires_minutes: int, secret: str):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)
