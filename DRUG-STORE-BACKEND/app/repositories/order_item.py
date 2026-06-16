from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order_item import OrderItemORM

class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create(self,order_item: OrderItemORM)->OrderItemORM:
        self.db.add(order_item)
        return order_item
