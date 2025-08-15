# app/api/routes/auth.py
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import RedirectResponse, JSONResponse
from jose import JWTError
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI
from app.services.google_oauth import exchange_code_for_tokens, get_user_info
from app.core.security import create_jwt_token, decode_jwt_token
from app.services.user_service import upsert_google_user
from app.services.token_service import issue_access_token, issue_refresh_token, validate_refresh_token

router = APIRouter()

@router.get("/google")
def google_login():
    try:
        logger.info("Initiating Google OAuth login.")
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={GOOGLE_REDIRECT_URI}"
            "&scope=openid%20email%20profile"
        )
        return RedirectResponse(google_auth_url)
    except Exception as e:
        logger.error(f"Error during Google login initiation: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Google login.")

@router.get("/google/callback")
def google_callback(code: str):
    try:
        logger.info("Handling Google OAuth callback.")
        token_data = exchange_code_for_tokens(code)
        user_info = get_user_info(token_data["access_token"])
        logger.info(f"User info retrieved: {user_info}")

        access_token = create_jwt_token(user_info["email"], expires_minutes=15)
        refresh_token = create_jwt_token(user_info["email"], expires_minutes=60*24*7)  # 7 days
        logger.info("Access and refresh tokens generated successfully.")

        return JSONResponse({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    except Exception as e:
        logger.error(f"Error during Google OAuth callback: {e}")
        raise HTTPException(status_code=500, detail="Failed to handle Google OAuth callback.")


@router.post("/refresh")
def refresh_access_token(refresh_token: str = Body(...)):
    try:
        payload = decode_jwt_token(refresh_token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access_token = create_jwt_token(email, expires_minutes=15)
        return {"access_token": new_access_token}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
