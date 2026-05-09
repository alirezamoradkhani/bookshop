from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import schemas, crud
from app.security import  get_current_user

from app.api.router import api_router
from app.workers.scheduler import scheduler
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

@app.on_event("startup")
async def startup():
    scheduler.start()


@app.get("/")
async def test():
    return "hello"

@app.get("/users/all", response_model=list[schemas.UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db), token_data: dict = Depends(get_current_user)):
    return await crud.get_all_users(db=db, token_data=token_data)


