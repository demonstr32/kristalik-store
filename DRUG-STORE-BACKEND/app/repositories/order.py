from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.order import OrderORM

class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    async def create(self,order: OrderORM)->OrderORM:
        self.db.add(order)

        await self.db.flush()
        return await self.get_by_id(order.id)
    async def get_by_user_id(self,user_id: UUID)->list[OrderORM]:
        res = await self.db.execute(select(OrderORM).where(OrderORM.user_id == user_id).options(selectinload(OrderORM.items)))
        return list(res.scalars().all())
    async def get_by_id(self, order_id: UUID)->OrderORM | None:
        res = await self.db.execute(select(OrderORM).where(OrderORM.id==order_id).options(selectinload(OrderORM.items)))
        return res.scalars().first()
    async def update_status(self,order_id: UUID, status: str)->OrderORM | None:
        up = await self.db.get(OrderORM, order_id)
        if up:
            up.status = status
            return up
        return None
    async def delete_order(self,order_id: UUID):
        order = await self.db.get(OrderORM,order_id)
        if order:
            await self.db.delete(order)
