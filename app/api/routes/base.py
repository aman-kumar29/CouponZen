from fastapi import APIRouter
from app.core.responses import success_response

router = APIRouter()

@router.get("/", tags=["Base"])
async def root():
    return {"message": "Welcome to the CouponZen API 🚀"}

@router.get("/health", tags=["Base"])
async def health_check():
    return success_response({"all_good": "yes"},"Server Running Properly!!!", 200)
