from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.base import DomainException

async def domain_exception_handler(request: Request, exc: Exception):  # ← Exception
    if isinstance(exc, DomainException):
        return JSONResponse(
            status_code=getattr(exc, "status_code", 400),
            content={"error": getattr(exc, "code", "UNKNOWN"), "message": getattr(exc, "message", str(exc))}
        )
    # اگر Exception دیگری است، می‌توانیم مجدداً raise کنیم یا default response بدهیم
    raise exc