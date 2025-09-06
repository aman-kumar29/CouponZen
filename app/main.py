# app/main.py (only the relevant parts changed)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logger import setup_logger
from app.api.routes import base, auth
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    internal_error_handler,
)
from app.db.session import init_db  # <-- async init
import os

logger = setup_logger(__name__)
app = FastAPI(title="CouponZen")

db_initialized: bool | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_error_handler)

@app.on_event("startup")
async def startup_event():
    global db_initialized
    logger.info("🚀 FastAPI server starting up...")
    logger.info(f"GOOGLE_CLIENT_ID available: {bool(os.getenv('GOOGLE_CLIENT_ID'))}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f".env file exists: {os.path.exists('.env')}")

    try:
        await init_db()       # ✅ await the async DB init (creates tables if missing)
        db_initialized = True
        logger.info("✅ Database initialization successful")
    except Exception as e:
        db_initialized = False
        logger.error(f"❌ Database initialization failed: {e}", exc_info=True)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 FastAPI server shutting down...")

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "database": "connected" if db_initialized else "disconnected"
    }

app.include_router(base.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
