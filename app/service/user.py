import bcrypt
import secrets
from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from app.utils.exception import CustomException, ExceptionEnum

class UserService:
    encoding = "UTF-8"
    jwt_algorithm = "HS256"
    secret_key = "b8394efc3c1d4838a71587c4b6aef2fb1a62dcbf4d9e4c4b8bfa86c279d768d4"
    
    async def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), 
            bcrypt.gensalt()
        )
        return hashed_password.decode("UTF-8")
    
    async def verfiy_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(self.encoding),
                              hashed_password.encode(self.encoding))
        
    async def create_jwt(self, userID: str) -> str:
        return jwt.encode(
            {
                "sub": userID,
                "exp": datetime.now() + timedelta(days=1)
            }, 
            self.secret_key, algorithm=self.jwt_algorithm
        )
    
    async def decode_jwt(self, access_token: str):
        try:
            payload: dict = jwt.decode(
                access_token, 
                self.secret_key, 
                algorithms=[self.jwt_algorithm]
            )            
            return payload['sub']
        
        except ExpiredSignatureError:
            raise CustomException(ExceptionEnum.TOKEN_EXPIRED)