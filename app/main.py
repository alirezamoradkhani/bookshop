from app.api.router import api_router

from app.exceptions.base import DomainException
from app.exceptions.exception_handler import domain_exception_handler

from app.ratelimiter.limiter import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
from app.dependency_injection.container import Container

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

container = Container()

container.wire(
    packages=[
        "app.api",
        "app.book.route",
        "app.user.route",
        "app.order.route",
        "app.edition.route",
        "app.borrow.route",
        "app.analytics.route",
        "app.transaction.route",
        "app.search.route",
    ]
)

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(api_router)
app.add_exception_handler(DomainException,domain_exception_handler)
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler) # type: ignore

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    logger.error("Unhandled request error", exc_info=(type(exc), exc, exc.__traceback__))
    return JSONResponse(status_code=500, content={"error": "INTERNAL_SERVER_ERROR", "message": "Internal server error"})

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}

@app.get("/", tags=["system"])
async def root():
    return {"service": "bookshop", "status": "ok"}




