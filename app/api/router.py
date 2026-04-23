from fastapi import APIRouter
from app.user.rout import router as user_router
from app.book.rout import router as book_router
from app.edition.rout import router as edition_router
from app.order.rout import router as order_router
from app.transaction.rout import router as transaction_router
from app.borrow.rout import router as borrow_router
from app.analytics.rout import router as analytics_router


api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(book_router)
api_router.include_router(edition_router)
api_router.include_router(order_router)
api_router.include_router(transaction_router)
api_router.include_router(borrow_router)
api_router.include_router(analytics_router)