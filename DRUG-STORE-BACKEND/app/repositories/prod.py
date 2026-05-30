from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.prod import ProductORM

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self)-> list[ProductORM]:
        return list(self.db.scalars(select(ProductORM)).all())
    
    def get_by_id(self, prod_id: int)->ProductORM | None:
        return self.db.scalars(select(ProductORM).where(ProductORM.id == prod_id)).first()
    def create(self, product: ProductORM)-> ProductORM:
        self.db.add(product)
        return product
    def delete(self,product: ProductORM)->None:
        self.db.delete(product)