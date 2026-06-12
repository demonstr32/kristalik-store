from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
class OrderItemORM(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"),nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"),nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)