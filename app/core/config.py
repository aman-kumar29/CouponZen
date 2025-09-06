import os
from dotenv import load_dotenv
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# Load environment variables from .env file
load_dotenv()
logger.info("Environment variables loaded successfully.")

# API settings
API_V1_STR = "/api/v1"
PROJECT_NAME = "CouponZen"

# Authentication
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Database
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATA = os.getenv("POSTGRES_DATA")

DATABASE_URL = os.getenv("DATABASE_URL")
# Other settings
SSL_CERT_DAYS = int(os.getenv("SSL_CERT_DAYS", "820"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# Log important settings (excluding secrets)
logger.debug("Settings loaded:")
logger.debug(f"ENVIRONMENT: {ENVIRONMENT}")
logger.debug(f"DEBUG: {DEBUG}")
logger.debug(f"POSTGRES_HOST: {POSTGRES_HOST}")
logger.debug(f"POSTGRES_DATABASE: {POSTGRES_DATABASE}")
logger.debug(f"GOOGLE_REDIRECT_URI: {GOOGLE_REDIRECT_URI}")
