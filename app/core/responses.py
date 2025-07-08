from fastapi.responses import JSONResponse
from typing import Any

def success_response(data: Any, message: str = "Success", status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "status_code": status_code,
            "message": message,
            "data": data
        }
    )
