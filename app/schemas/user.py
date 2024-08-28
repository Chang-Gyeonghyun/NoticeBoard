from pydantic import BaseModel, ConfigDict

class UserLogin(BaseModel):
    userID: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)
    
class UserSignup(UserLogin):
    email: str
    userName: str
    phone: str
    birthday: str
    address: str
    
    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(UserSignup):
    pass

class UserProfileResponse(BaseModel):
    id: int
    userID: str
    email: str
    userName: str
    phone: str
    birthday: str
    address: str
    
    model_config = ConfigDict(from_attributes=True)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    