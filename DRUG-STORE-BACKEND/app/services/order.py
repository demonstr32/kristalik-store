from uuid import UUID
from sqlalchemy.orm import Session
from app.models.order import OrderORM
from app.models.order_item import OrderItemORM
from app.repositories.order import OrderRepository
from app.repositories.order_item import OrderItemRepository
from app.repositories.cart import CartRepository
from app.repositories.cart_item import CartItemRepository
from app.schemas.order import OrderCreateSchema, OrderItemResponseSchema, OrderResponseSchema, OrderUpdateSchema
from app.schemas.cart import CartResponseSchema
from app.repositories.prod import ProductRepository
class NoCartItem(Exception):
    """корзина пустая"""
class OrderNotFound(Exception):
    """Заказ не найден"""

class NotUserOrder(Exception):
    """Заказ принадлежит другому пользователю"""

class OrderCannotBeCancelled(Exception):
    """Нельзя отменить заказ в текущем статусе"""
class OrderService:
    def __init__(self,db: Session):
        self.db = db
        self.order_repository = OrderRepository(db)
        self.order_item_repository = OrderItemRepository(db)
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
    def create_order(self, user_id: UUID)->OrderResponseSchema:
        cart = self.cart_repository.get_or_create(user_id)
        cart_item = self.cart_item_repository.get_by_cart_id(cart.id)
        if not cart_item:
            raise NoCartItem()
        
        total_price = 0
        for c in cart_item:
            product = self.product_repository.get_by_id(c.product_id)
            if product:
                total_price+= product.price*c.quantity
        order = OrderORM(user_id=user_id,total_price=total_price)
        self.order_repository.create(order)
        self.db.commit()
        self.db.refresh(order)


        for c in cart_item:
            product = self.product_repository.get_by_id(c.product_id)
            order_item = OrderItemORM(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=c.quantity
        
            )
            self.order_item_repository.create(order_item)
        self.cart_item_repository.clear_cart(cart.id)
        self.db.commit()
        return OrderResponseSchema.model_validate(order)
    def get_user_orders(self,user_id: UUID)->list[OrderResponseSchema]:
        orders = self.order_repository.get_by_user_id(user_id)
        return [OrderResponseSchema.model_validate(o) for o in orders]
    def get_order(self, order_id: UUID, user_id: UUID)->OrderResponseSchema:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        if order.user_id!=user_id:
            raise NotUserOrder()
        return OrderResponseSchema.model_validate(order)
    def update_order_status(self,order_id: UUID, status: str)->OrderResponseSchema:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        self.order_repository.update_status(order_id=order.id,status=status)
        self.db.commit()
        self.db.refresh(order)
        return OrderResponseSchema.model_validate(order)
    def cancel_order(self,order_id: UUID, user_id: UUID)->OrderResponseSchema:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        if order.user_id!=user_id:
            raise NotUserOrder()
        if order.status!="pending":
            raise OrderCannotBeCancelled()
        self.update_order_status(order_id=order.id,status="cancelled")

        return OrderResponseSchema.model_validate(order)