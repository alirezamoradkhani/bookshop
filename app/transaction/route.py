from fastapi import APIRouter, Depends, Request
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.transaction.services.command.deposit import deposit
from app.transaction.services.command.transfer import transfer
from app.transaction.services.querys.wallet_info import walletinfo
from app.transaction.services.command.withdraw import withdraw
from app.transaction.schemas.outputs import BaseUserResponse
from app.Idempotency.dependency import get_idempotency_handler
from app.Idempotency.get_idempotency_key import get_idempotency_key
from app.ratelimiter.limiter import limiter


router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/deposit")
@limiter.limit("5/minute")
async def Deposit(request: Request, amount:int, handeler = Depends(get_idempotency_handler), uow = Depends(get_uow),toke_data = Depends(get_current_user),idempotency_key: str = Depends(get_idempotency_key)):
    # return await deposit(uow=uow,token_data=toke_data,amount=amount)
    return await handeler(key=idempotency_key,usecase=deposit,uow=uow,token_data=toke_data,amount=amount)

@router.post("/transfer",response_model=BaseUserResponse)
@limiter.limit("5/minute")
async def Transfer(request: Request, amount:int,reciver_id:int ,handeler = Depends(get_idempotency_handler), uow = Depends(get_uow),toke_data = Depends(get_current_user),idempotency_key: str = Depends(get_idempotency_key)):
    # return await transfer(uow=uow,token_data=toke_data,amount=amount,reciver_id=reciver_id)
    return await handeler(key=idempotency_key,usecase=transfer,uow=uow,token_data=toke_data,amount=amount,reciver_id=reciver_id)

@router.get("/info")
@limiter.limit("5/minute")
async def wallet_info(request: Request, uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await walletinfo(uow=uow,token_data=toke_data)

@router.post("/withdraw",response_model=BaseUserResponse)
@limiter.limit("5/minute")
async def Withdraw(request: Request, amount:int, handeler = Depends(get_idempotency_handler), uow = Depends(get_uow),toke_data = Depends(get_current_user),idempotency_key: str = Depends(get_idempotency_key)):
    # return await withdraw(uow=uow,token_data=toke_data,amount=amount)
    return await handeler(key=idempotency_key,usecase=withdraw,uow=uow,token_data=toke_data,amount=amount)
