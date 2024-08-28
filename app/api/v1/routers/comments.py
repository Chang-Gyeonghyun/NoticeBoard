from fastapi import APIRouter, Body, Depends
from app.core.security import get_access_token
from app.db.repository.comments import CommentRepository
from app.db.repository.posts import PostRepository
from app.db.repository.user import UserRepository
from app.models.models import Comment, Post, User
from app.schemas.comments import CommentCreate
from app.service.user import UserService
from app.utils.exception import CustomException, ExceptionEnum

router = APIRouter(prefix="/posts")

@router.post("/{post_id}/comments", status_code=201)
async def create_comment(
    post_id: int,
    request: CommentCreate = Body(...),
    access_token: str = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    comment_repo: CommentRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    post: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not post:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)
    await comment_repo.create_comment(post_id=post.id, user_id=user.id, request=request)

@router.post("/{post_id}/comments/{comment_id}/replies", status_code=201)
async def create_reply(
    post_id: int,
    comment_id: int,
    request: CommentCreate = Body(...),
    access_token: str = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    comment_repo: CommentRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    post: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not post:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)
    comment: Comment | None = await comment_repo.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise CustomException(ExceptionEnum.COMMENT_NOT_FOUND)
    
    await comment_repo.create_reply(
        post_id=post.id,
        user_id=user.id,
        parent_comment_id=comment.id,
        content=request.content
    )


@router.post("/{post_id}/comments/{comment_id}/like")
async def like_comment(
    post_id: int,
    comment_id: int,
    access_token: str = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    comment_repo: CommentRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    post: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not post:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)  
    comment: Comment | None = await comment_repo.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise CustomException(ExceptionEnum.COMMENT_NOT_FOUND)
    await comment_repo.like_comment(user=user, comment=comment)

@router.post("/{post_id}/comments/{comment_id}/dislike")
async def dislike_comment(
    post_id: int,
    comment_id: int,
    access_token: str = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    comment_repo: CommentRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    post: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not post:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)  
    comment: Comment | None = await comment_repo.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise CustomException(ExceptionEnum.COMMENT_NOT_FOUND)
    await comment_repo.dislike_comment(user=user, comment=comment)
    
@router.delete("/{post_id}/comments/{comment_id}", status_code=204)
async def delete_comment(
    post_id: int,
    comment_id: int,
    access_token: str = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    comment_repo: CommentRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    post: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not post:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)  
    comment: Comment | None = await comment_repo.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise CustomException(ExceptionEnum.COMMENT_NOT_FOUND)
    if user.id != comment.user_id:
        raise CustomException(ExceptionEnum.FORBIDDEN)
    
    await comment_repo.delete_comment(comment_id=comment_id)