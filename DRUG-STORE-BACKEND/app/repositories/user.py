from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.user import UserORM

class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: EmailStr)->UserORM | None:
        return self.db.scalars(select(UserORM).where(UserORM.email == email)).first()

    def get_user_by_id(self, user_id: UUID)-> UserORM | None:
        return self.db.get(UserORM, user_id)

    def create_user(self, email: EmailStr, hashed_password: str)-> UserORM:
        new_user = UserORM(email=email, hashed_password=hashed_password)
        self.db.add(new_user)
        return new_user
    
    def delete_user(self, user: UserORM)->None:
        self.db.delete(user)