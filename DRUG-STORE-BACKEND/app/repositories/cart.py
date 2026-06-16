from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cart import CartORM
from uuid import UUID

class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_by_id(self, cart_id: UUID) -> CartORM | None:
        return await self.db.get(CartORM, cart_id)
    async def get_or_create(self,user_id: UUID)->CartORM:
        res = await self.db.execute(select(CartORM).where(CartORM.user_id==user_id))
        get = res.scalars().first()
        if get is not None:
            return get
        else:
            new_cart = CartORM(user_id=user_id)
            self.db.add(new_cart)
            return new_cart
    