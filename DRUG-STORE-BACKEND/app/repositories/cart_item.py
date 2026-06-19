from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cart_item import CartItemORM

class CartItemRepository:
    def __init__(self,db: AsyncSession) -> None:
        self.db = db
    async def get_by_cart_id(self,cart_id: UUID)->list[CartItemORM]:
        res = await self.db.execute(select(CartItemORM).where(CartItemORM.cart_id==cart_id))
        return list(res.scalars().all())
    async def get_by_id(self, item_id: int) -> CartItemORM | None:
        return await self.db.get(CartItemORM, item_id)
    async def get_by_cart_and_product(self,cart_id: UUID, product_id: int)->CartItemORM | None:
        res = await self.db.execute(select(CartItemORM).where(CartItemORM.cart_id==cart_id, CartItemORM.product_id==product_id))
        return res.scalars().first()

    async def add_item(self,cart_id: UUID, product_id: int, quantity: int)->CartItemORM:
        new_item = CartItemORM(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self.db.add(new_item)
        return new_item
    async def update_quantity(self,item_id: int, quantity: int)->CartItemORM | None:
        item = await self.db.get(CartItemORM, item_id)
        if item:
            item.quantity = quantity
            return item
        return None
    async def remove_item(self, item_id: int)->None:
        item = await self.db.get(CartItemORM, item_id)
        if item: 
            self.db.delete(item)
    async def clear_cart(self, cart_id: UUID)->None:
        await self.db.execute(delete(CartItemORM).where(CartItemORM.cart_id==cart_id))
