# app/main.py
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

logger = setup_logger(__name__)
app = FastAPI(title="CouponZen")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_error_handler)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI server starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 FastAPI server shutting down...")

# Routers
app.include_router(base.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
