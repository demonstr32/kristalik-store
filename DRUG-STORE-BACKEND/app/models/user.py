from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class UserORM(Base):
    __tablename__ = "users"
    user_id: Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_admin: Mapped[bool] = mapped_column(default=False)