from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import  select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserORM

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_user_by_email(self, email: EmailStr)->UserORM | None:
        res =  await self.db.execute(select(UserORM).where(UserORM.email == email))
        return res.scalars().first()
    async def get_user_by_id(self, user_id: UUID)-> UserORM | None:
        return await self.db.get(UserORM, user_id)

    async def create_user(self, email: EmailStr, hashed_password: str)-> UserORM:
        new_user = UserORM(email=email, hashed_password=hashed_password)
        self.db.add(new_user)
        return new_user
    
    async def delete_user(self, user: UserORM)->None:
        self.db.delete(user)