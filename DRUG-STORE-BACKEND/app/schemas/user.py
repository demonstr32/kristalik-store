from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
class UserUpdateSchema(BaseModel):
    email: EmailStr | None=None
    password: str | None=None
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: UUID = Field(validation_alias="user_id")
    email: EmailStr
class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema