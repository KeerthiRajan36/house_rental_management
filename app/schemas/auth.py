from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from app.models.user import UserRole


class RegisterRequest(BaseModel):

    full_name: str
    email: EmailStr
    password: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):

    id: int
    full_name: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)