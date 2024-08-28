from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.exception import CustomException, ExceptionEnum

def get_access_token(
    auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=True)) 
) -> str:
    if auth_header is None:
        raise CustomException(ExceptionEnum.UNAUTHORIZED)
    return auth_header.credentials