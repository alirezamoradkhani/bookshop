from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.transaction.services.deposit import deposit
from app.transaction.services.transfer import transfer
from app.transaction.schemas.outputs import BaseUserResponse


router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/deposit",response_model=BaseUserResponse)
async def Deposit(amount:int,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await deposit(uow=uow,token_data=toke_data,amount=amount)

@router.post("/transfer",response_model=BaseUserResponse)
async def Transfer(amount:int,reciver_id:int ,uow = Depends(get_uow),toke_data = Depends(get_current_user)):
    return await transfer(uow=uow,token_data=toke_data,amount=amount,reciver_id=reciver_id)