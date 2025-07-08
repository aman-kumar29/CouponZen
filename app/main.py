from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import setup_logger
from app.api.routes import base, video, summary, chat
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import (
    http_exception_handler,
    internal_error_handler,
    validation_exception_handler,
    service_unavailable_handler
)


logger = setup_logger(__name__)

app = FastAPI(title="YouTube Chat Summarizer")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_error_handler)

# Startup/Shutdown logs
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI server starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 FastAPI server shutting down...")

# Base + Placeholder Routes
app.include_router(base.router)                # / and /health
# app.include_router(video.router, prefix="/video", tags=["Video"])
# app.include_router(summary.router, prefix="/summary", tags=["Summary"])
# app.include_router(chat.router, prefix="/chat", tags=["Chat"])
