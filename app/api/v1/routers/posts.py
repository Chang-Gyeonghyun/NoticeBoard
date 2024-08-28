from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.core.security import get_access_token
from app.db.repository.attachments import AttachmentRepository
from app.db.repository.posts import PostRepository
from app.db.repository.user import UserRepository
from app.models.models import Attachment, Post, User
from app.schemas.posts import PostRequest, PostUpdateRequest, PostsByPaging, PostInstance, PostBase
from app.service.attachment import AttachmentService
from app.service.post import PostService
from app.service.user import UserService
from app.utils.exception import CustomException, ExceptionEnum

router = APIRouter(prefix="/posts")

@router.post("/create", status_code=201)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    files: List[UploadFile] = File(),
    access_token = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    attach_service: AttachmentService = Depends(),
    attach_repo: AttachmentRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    request = PostRequest(title=title, content=content)
    post: Post = await post_repo.create_post(post_form=request, user=user)
    if files:
        urls, file_name = await attach_service.upload_to_s3(files)
        await attach_repo.save_files(post_id=post.id, file_urls=urls, file_name=file_name)
    
    
@router.get("")
async def get_all_post_by_paging(
    pageNo: int,
    pageSize: int,
    post_repo: PostRepository = Depends(),
    post_service: PostService = Depends()
):
    query = post_service.create_search_query()
    items, total_page = await post_repo.get_posts_by_page(query=query,pageNo=pageNo, pageSize=pageSize)
    
    result_items = [PostBase.model_validate(item, from_attributes=True) for item in items]
    return PostsByPaging(
        currentPage=pageNo,
        items=result_items,
        pageSize=pageSize,
        totalSize=total_page
    )

@router.get("/search")
async def get_filter_post_by_paging(
    pageNo: int,
    pageSize: int,
    entire: str | None = None,
    userName: str | None = None,
    title: str | None = None,
    post_repo: PostRepository = Depends(),
    post_service: PostService = Depends()
):
    query = post_service.create_search_query(entire=entire, userName=userName, title=title)
    items, total_page = await post_repo.get_posts_by_page(query=query, pageNo=pageNo, pageSize=pageSize)
    
    result_items = [PostBase.model_validate(item, from_attributes=True) for item in items]
    return PostsByPaging(
        currentPage=pageNo,
        items=result_items,
        pageSize=pageSize,
        totalSize=total_page
    )
    
@router.get("/{post_id}")
async def get_post_instance(
    post_id: int,
    post_repo: PostRepository = Depends(),
    post_service: PostService = Depends()
):
    item: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not item:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)
    item: PostInstance = PostInstance.model_validate(item, from_attributes=True)
    item.comments = await post_service.build_comment_tree(item.comments)
    return item


@router.delete("/delete/{post_id}", status_code=204)
async def delete_post_instance(
    post_id: int,
    access_token: str = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    item: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not item:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)
    if user.id != item.user_id:
        raise CustomException(ExceptionEnum.FORBIDDEN)
    await post_repo.delete_post(post_id=post_id)
    
@router.put("/update/{post_id}", status_code=200)
async def update_post(
    post_id: int,
    post_data: PostUpdateRequest,
    access_token = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends()
):
    userID: str = await user_service.decode_jwt(access_token=access_token)
    user: User | None = await user_repo.search_user_by_id(userID=userID)
    if not user:
        raise CustomException(ExceptionEnum.USER_NOT_FOUND)
    item: Post | None = await post_repo.get_post_by_id(post_id=post_id)
    if not item:
        raise CustomException(ExceptionEnum.POST_NOT_FOUND)
    if user.id != item.user_id:
        raise CustomException(ExceptionEnum.FORBIDDEN)
    await post_repo.update_post(post_id=post_id, post_data=post_data)
    
@router.post("/{post_id}/like", status_code=200)
async def like_post(
    post_id: int,
    access_token = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
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
    await post_repo.like_post(user, post)

@router.post("/{post_id}/dislike", status_code=200)
async def dislike_post(
    post_id: int,
    access_token = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
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
    await post_repo.dislike_post(user, post)

@router.get("/{post_id}/download/{attachment_id}", status_code=200)
async def dislike_post(
    post_id: int,
    attachment_id: int,
    access_token = Depends(get_access_token),
    post_repo: PostRepository = Depends(),
    attach_repo: AttachmentRepository = Depends(),
    attach_service: AttachmentService = Depends(),
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
    attachment: Attachment | None = await attach_repo.get_file_by_id(attachment_id)
    if not attachment:
        raise CustomException(ExceptionEnum.FILE_NOT_FOUND)
    file = await attach_service.download_file(attachment=attachment)
    return file