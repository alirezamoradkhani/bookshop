from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.security import get_current_user
from app.user.services.command.authenticate import login_by_user_pass, login_by_otp
from app.user.services.command.create_baseuser import create_user, email_register
from app.user.services.command.delete_account import delete_account
from app.user.services.command.upgrade_user_plan import upgrade_plan
from app.user.services.querys.search_author import search_author
from app.get_unit_of_work import get_uow
from app.user.schemas import inputs, outputs

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/singin")
async def Verify_email(email: str,uow = Depends(get_uow)):
    return await email_register(email=email,uow=uow)
    
@router.post("/create", response_model= outputs.BaseUserResponse)
async def Create_user(user: inputs.UserCreate, otp:str, uow = Depends(get_uow)):
    return await create_user(uow=uow,user=user,otp=otp)

@router.post("/login")
async def login_step_one(user: inputs.UserLogin,uow = Depends(get_uow)):
    return await login_by_user_pass(uow=uow,user=user)

# @router.post("/login_by_otp", response_model=outputs.TokenResponse)
# async def login(email:str,otp :str, uow = Depends(get_uow)):
#     return await login_by_otp(uow=uow,otp=otp,email=email)

@router.delete("/delete", response_model= outputs.BaseUserResponse)
async def Delete_account(token_data: dict = Depends(get_current_user), uow = Depends(get_uow)):
    return await delete_account(uow=uow,token_data=token_data)

@router.patch("/plan",response_model= outputs.UserResponse)
async def Upgrade_plan(new_plan:inputs.UserPlanUpgrade,token_data: dict = Depends(get_current_user),uow = Depends(get_uow)):
    return await upgrade_plan(uow=uow,new_plan=new_plan, token_data=token_data)

@router.get("/author/search",response_model=list[outputs.AuthorResponse])
async def Search_author(name:str | None=None,id:int | None=None,uow=Depends(get_uow)):
    return await search_author(uow=uow,name=name,id=id)