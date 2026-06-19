from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import OrderORM
import asyncio
from app.models.order_item import OrderItemORM
from app.repositories.order import OrderRepository
from app.repositories.order_item import OrderItemRepository
from app.repositories.cart import CartRepository
from app.repositories.cart_item import CartItemRepository
from app.schemas.order import  OrderItemResponseSchema, OrderResponseSchema, OrderUpdateSchema
from app.schemas.cart import CartResponseSchema
from app.repositories.prod import ProductRepository
class NoProduct(Exception):
    """возможно продукт был удален"""
class NoCartItem(Exception):
    """корзина пустая"""
class OrderNotFound(Exception):
    """Заказ не найден"""

class NotUserOrder(Exception):
    """Заказ принадлежит другому пользователю"""

class OrderCannotBeCancelled(Exception):
    """Нельзя отменить заказ в текущем статусе"""
class OrderService:
    def __init__(self,db: AsyncSession):
        self.db = db
        self.order_repository = OrderRepository(db)
        self.order_item_repository = OrderItemRepository(db)
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
    async def create_order(self, user_id: UUID)->OrderResponseSchema:
        cart = await self.cart_repository.get_or_create(user_id)
        cart_item = await self.cart_item_repository.get_by_cart_id(cart.id)
        if not cart_item:
            raise NoCartItem()
        order =OrderORM(user_id=user_id, total_price=0)
        await self.order_repository.create(order)
        await self.db.flush()
        tasks = []
        for i in cart_item:
            product = self.product_repository.get_by_id(i.product_id)
            tasks.append(product)
        result  = await asyncio.gather(*tasks)
        total_price = 0
        for c, product in zip(cart_item,result):
            
            if not product:
                raise NoProduct()
            total_price += product.price * c.quantity

            order_item = OrderItemORM(
                order_id = order.id,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=c.quantity
            )
            await self.order_item_repository.create(order_item)
        order.total_price = total_price
        await self.cart_item_repository.clear_cart(cart.id)
        await self.db.commit()
        ready_order = await self.order_repository.get_by_id(order.id)

        return OrderResponseSchema.model_validate(ready_order)
    async def get_user_orders(self,user_id: UUID)->list[OrderResponseSchema]:
        orders = await self.order_repository.get_by_user_id(user_id)
        return [OrderResponseSchema.model_validate(o) for o in orders]
    async def get_order(self, order_id: UUID, user_id: UUID)->OrderResponseSchema:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        if order.user_id!=user_id:
            raise NotUserOrder()
        return OrderResponseSchema.model_validate(order)
    async def update_order_status(self,order_id: UUID, status: str)->OrderResponseSchema:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        await self.order_repository.update_status(order_id=order.id,status=status)
        await self.db.commit()
        await self.db.refresh(order)
        return OrderResponseSchema.model_validate(order)
    async def cancel_order(self,order_id: UUID, user_id: UUID)->OrderResponseSchema:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        if order.user_id!=user_id:
            raise NotUserOrder()
        if order.status!="pending":
            raise OrderCannotBeCancelled()
        await self.update_order_status(order_id=order.id,status="cancelled")

        return OrderResponseSchema.model_validate(order)
    async def delete_order(self,order_id: UUID)->None:
        await self.order_repository.delete_order(order_id)
        await self.db.commit()