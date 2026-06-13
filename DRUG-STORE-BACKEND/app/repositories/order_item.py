from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.order_item import OrderItemORM

class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self,order_item: OrderItemORM)->OrderItemORM:
        self.db.add(order_item)
        return order_item
