from fastapi import APIRouter, Depends,Header
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.transaction.services.command.deposit import deposit
from app.transaction.services.command.transfer import transfer
from app.transaction.services.querys.wallet_info import walletinfo
from app.transaction.services.command.withdraw import withdraw
from app.transaction.schemas.outputs import BaseUserResponse
from app.Idempotency.dependency import get_idempotency_handler
from app.Idempotency.get_idempotency_key import get_idempotency_key


router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/deposit")
async def Deposit(amount:int,uow = Depends(get_uow),toke_data = Depends(get_current_user),idempotency_key: str = Depends(get_idempotency_key)):
    # return await deposit(uow=uow,token_data=toke_data,amount=amount)
    handeler = get_idempotency_handler()
    return await handeler(key=idempotency_key,usecase=deposit,uow=uow,token_data=toke_data,amount=amount)

@router.post("/transfer",response_model=BaseUserResponse)
async def Transfer(amount:int,reciver_id:int ,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await transfer(uow=uow,token_data=toke_data,amount=amount,reciver_id=reciver_id)

@router.get("/info")
async def wallet_info(uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await walletinfo(uow=uow,token_data=toke_data)

@router.post("/withdraw",response_model=BaseUserResponse)
async def Withdraw(amount:int,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await withdraw(uow=uow,token_data=toke_data,amount=amount)
