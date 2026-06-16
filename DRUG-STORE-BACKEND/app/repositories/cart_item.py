from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.cart_item import CartItemORM

class CartItemRepository:
    def __init__(self,db: Session) -> None:
        self.db = db
    def get_by_cart_id(self,cart_id: UUID)->list[CartItemORM]:
        return list(self.db.scalars(select(CartItemORM).where(CartItemORM.cart_id==cart_id)).all())
    def get_by_id(self, item_id: int) -> CartItemORM | None:
        return self.db.get(CartItemORM, item_id)
    def get_by_cart_and_product(self,cart_id: UUID, product_id: int)->CartItemORM | None:
        return self.db.scalars(select(CartItemORM).where(CartItemORM.cart_id==cart_id, CartItemORM.product_id==product_id)).first()

    def add_item(self,cart_id: UUID, product_id: int, quantity: int)->CartItemORM:
        new_item = CartItemORM(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self.db.add(new_item)
        return new_item
    def update_quantity(self,item_id: int, quantity: int)->CartItemORM | None:
        item = self.db.get(CartItemORM, item_id)
        if item:
            item.quantity = quantity
            return item
        return None
    def remove_item(self, item_id: int)->None:
        item = self.db.get(CartItemORM, item_id)
        if item: 
            self.db.delete(item)
    def clear_cart(self, cart_id: UUID)->None:
        items = self.db.scalars(select(CartItemORM).where(CartItemORM.cart_id==cart_id)).all()
        for item in items:
            self.db.delete(item)
