import requests
from fastapi import HTTPException
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

def exchange_code_for_tokens(code: str):
    try:
        logger.info("Exchanging authorization code for tokens.")
        token_resp = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        ).json()
        if "error" in token_resp:
            logger.error(f"Error in token response: {token_resp}")
            raise HTTPException(status_code=400, detail=token_resp)
        logger.info("Tokens exchanged successfully.")
        return token_resp
    except Exception as e:
        logger.error(f"Error during token exchange: {e}")
        raise

def get_user_info(access_token: str):
    try:
        logger.info("Fetching user info from Google.")
        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        logger.info("User info retrieved successfully.")
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        raise