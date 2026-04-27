# interface/api/exception_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.base import DomainException

async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=getattr(exc, "status_code", 400),
        content={"error": exc.code, "message": exc.message}
    )