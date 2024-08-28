from typing import List
from fastapi import APIRouter, Body, Depends
from app.core.security import get_access_token
from app.db.repository.posts import PostRepository
from app.service.user import UserService
from app.db.repository.user import UserRepository
from app.models.models import Post, User
import app.schemas.user as user_schema
from app.utils.exception import CustomException, ExceptionEnum

router = APIRouter(prefix="/user")

@router.post("/sign-up", response_model=user_schema.LoginResponse)
async def user_sign_up(
        request: user_schema.UserSignup,
        user_repo: UserRepository = Depends(),
        user_service: UserService = Depends()
    ):
    if await user_repo.search_user_by_id(request.userID):
        raise CustomException(ExceptionEnum.USER_EXISTS)
    
    request.password = await user_service.hash_password(request.password)
    user: User = await user_repo.create_user(request)
    access_token = await user_service.create_jwt(user.userID)
    return user_schema.LoginResponse(access_token=access_token)

@router.post("/sign-in", response_model=user_schema.LoginResponse)
async def user_sign_in(
        request: user_schema.UserLogin,
        user_repo: UserRepository = Depends(),
        user_service: UserService = Depends()
    ):
    user: User = await user_repo.search_user_by_id(request.userID)
    if not user:
        raise CustomException(ExceptionEnum.LOGIN_FAILED)
    
    if not await user_service.verfiy_password(plain_password=request.password, 
                                            hashed_password=user.password):
        raise CustomException(ExceptionEnum.LOGIN_FAILED)
    
    access_token = await user_service.create_jwt(user.userID)
    return user_schema.LoginResponse(access_token=access_token)\
        
@router.get("/profile", response_model=user_schema.UserProfileResponse)
async def get_user_profile(
    access_token: str = Depends(get_access_token),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    return user

@router.put("/update/{user_id}", response_model=user_schema.UserProfileResponse)
async def update_user_profile(
    user_id: int,
    request: user_schema.UserUpdate = Body(...),
    access_token: str = Depends(get_access_token),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    if user.id != user_id:
        raise CustomException(ExceptionEnum.FORBIDDEN)
    user = await user_repo.update_user(user=user, update_request=request)
    return user

@router.get("/posts")
async def get_post_by_user(
    access_token: str = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    return user.posts