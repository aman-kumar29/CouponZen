from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE
import logging

logger = logging.getLogger("uvicorn.error")


def create_error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "status_code": status_code,
            "message": message
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
    return create_error_response(exc.status_code, exc.detail)

async def internal_error_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)} | Path: {request.url.path} | Method: {request.method}")
    return create_error_response(HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")

async def validation_exception_handler(request: Request, exc):
    logger.warning("Validation Error")
    return create_error_response(422, "Validation Failed")

async def service_unavailable_handler(request: Request, exc: Exception):
    return create_error_response(HTTP_503_SERVICE_UNAVAILABLE, "Service temporarily unavailable")
