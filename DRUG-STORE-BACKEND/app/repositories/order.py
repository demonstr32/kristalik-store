from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.order import OrderORM

class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    def create(self,order: OrderORM)->OrderORM:
        self.db.add(order)
        return order
    def get_by_user_id(self,user_id: UUID)->list[OrderORM]:
        return list(self.db.scalars(select(OrderORM).where(OrderORM.user_id == user_id)).all())
    def get_by_id(self, order_id: UUID)->OrderORM | None:
        return self.db.scalars(select(OrderORM).where(OrderORM.id==order_id)).first()
    def update_status(self,order_id: UUID, status: str)->OrderORM | None:
        up = self.db.get(OrderORM, order_id)
        if up:
            up.status = status
            return up
        return None
    def delete_order(self,order_id: UUID):
        order = self.db.get(OrderORM,order_id)
        if order:
            self.db.delete(order)
