from app.api.router import api_router

from app.exceptions.base import DomainException
from app.exceptions.exception_handler import domain_exception_handler

from app.ratelimiter.limiter import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from fastapi import FastAPI
from app.dependency_injection.container import Container

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

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


@app.get("/")
async def test():
    return "hello"




