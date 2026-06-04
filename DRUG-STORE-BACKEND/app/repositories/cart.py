from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.cart import CartORM
from uuid import UUID

class CartRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_by_user_id(self, user_id: UUID)->CartORM | None:
        return self.db.scalars(select(CartORM).where(CartORM.user_id==user_id)).first()
    
    def create(self, user_id: UUID)->CartORM:
        new_cart = CartORM(user_id=user_id)
        self.db.add(new_cart)
        return new_cart
    def get_or_create(self,user_id: UUID)->CartORM:
        get = self.db.scalars(select(CartORM).where(CartORM.user_id==user_id)).first()
        if get is not None:
            return get
        else:
            new_cart = self.create(user_id)
            return new_cart
    