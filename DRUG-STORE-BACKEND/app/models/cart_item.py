from .base import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class CartItemORM(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cart_id: Mapped[UUID] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)