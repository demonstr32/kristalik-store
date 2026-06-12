from sqlalchemy import func
from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class OrderORM(Base):
    __tablename__ = "orders"
    id: Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"),nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    total_price: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="pending",nullable=False)
    items: Mapped[list["OrderItemORM"]] = relationship(back_populates="order")