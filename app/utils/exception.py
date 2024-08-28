from enum import Enum

class ExceptionEnum(Enum):
    BAD_REQUEST = ("아이디 혹은 비밀번호가 틀렸습니다.", 400)
    LOGIN_FAILED = ("Bad Request", 400)
    UNAUTHORIZED = ("Unauthorized", 401)
    TOKEN_EXPIRED = ("로그인 세션이 만료되었습니다.", 401)
    FORBIDDEN = ("Forbidden", 403)
    USER_NOT_FOUND = ("User Not Found", 404)
    POST_NOT_FOUND = ("Post Not Found", 404)
    COMMENT_NOT_FOUND = ("Comment Not Found", 404)
    FILE_NOT_FOUND = ("File Not Found", 404)
    USER_EXISTS = ("이미 사용 중인 아이디입니다.", 409)

    def __init__(self, detail, status_code):
        self.detail = detail
        self.status_code = status_code

class CustomException(Exception):
    def __init__(self, exception_enum: ExceptionEnum):
        self.detail = exception_enum.detail
        self.status_code = exception_enum.status_code

