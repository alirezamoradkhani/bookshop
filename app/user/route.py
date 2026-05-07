from fastapi import APIRouter, Depends, Request
from app.security import get_current_user
from app.user.services.command.authenticate import login_by_user_pass
from app.user.services.command.create_baseuser import create_user, email_register
from app.user.services.command.delete_account import delete_account
from app.user.services.command.upgrade_user_plan import upgrade_plan
from app.user.services.querys.search_author import search_author
from app.get_unit_of_work import get_uow
from app.user.schemas import inputs, outputs
from app.ratelimiter.limiter import limiter


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/singin")
@limiter.limit("5/minute")
async def Verify_email(request: Request, email: str,uow = Depends(get_uow)):
    return await email_register(email=email,uow=uow)
    
@router.post("/create", response_model= outputs.BaseUserResponse)
@limiter.limit("5/minute")
async def Create_user(request: Request, user: inputs.UserCreate, otp:str, uow = Depends(get_uow)):
    return await create_user(uow=uow,user=user,otp=otp)

@router.post("/login")
@limiter.limit("5/minute")
async def login_step_one(request: Request, user: inputs.UserLogin,uow = Depends(get_uow)):
    return await login_by_user_pass(uow=uow,user=user)

# @router.post("/login_by_otp", response_model=outputs.TokenResponse)
# async def login(email:str,otp :str, uow = Depends(get_uow)):
#     return await login_by_otp(uow=uow,otp=otp,email=email)

@router.delete("/delete", response_model= outputs.BaseUserResponse)
@limiter.limit("5/minute")
async def Delete_account(request: Request, token_data: dict = Depends(get_current_user), uow = Depends(get_uow)):
    return await delete_account(uow=uow,token_data=token_data)

@router.patch("/plan",response_model= outputs.UserResponse)
@limiter.limit("5/minute")
async def Upgrade_plan(request: Request, new_plan:inputs.UserPlanUpgrade,token_data: dict = Depends(get_current_user),uow = Depends(get_uow)):
    return await upgrade_plan(uow=uow,new_plan=new_plan, token_data=token_data)

@router.get("/author/search",response_model=list[outputs.AuthorResponse])
@limiter.limit("5/minute")
async def Search_author(request: Request, name:str | None=None,id:int | None=None,uow=Depends(get_uow)):
    return await search_author(uow=uow,name=name,id=id)