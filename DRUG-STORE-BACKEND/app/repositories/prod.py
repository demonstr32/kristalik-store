from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prod import ProductORM

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self)-> list[ProductORM]:
        res = await self.db.execute(select(ProductORM))
        return list(res.scalars().all())
    
    async def get_by_id(self, prod_id: int)->ProductORM | None:
        res = await self.db.execute(select(ProductORM).where(ProductORM.id == prod_id))
        return res.scalars().first()
    async def create(self, product: ProductORM)-> ProductORM:
        self.db.add(product)
        return product
    async def delete(self,product: ProductORM)->None:
        await self.db.delete(product)