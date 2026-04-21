from fastapi import APIRouter
from app.user.rout import router as user_router
from app.book.rout import router as book_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(book_router)