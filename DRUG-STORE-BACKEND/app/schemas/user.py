from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdateSchema(BaseModel):
    email: EmailStr | None=None
    password: str | None=None
    is_admin: bool | None=None
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: UUID
    email: EmailStr
    is_admin: bool
class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema