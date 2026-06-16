from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.prod import ProductRepository
from app.schemas.prod import ProductCreateSchema, ProductUpdateSchema, ProductResponseSchema
from app.models.prod import ProductORM

class ProductNotFound(Exception):
    """Товар не найден"""

class ProductService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.product_repository = ProductRepository(db)

    async def list_prod(self)->list[ProductResponseSchema]:
        products= await self.product_repository.get_all()
        return [ProductResponseSchema.model_validate(p) for p in products]
    
    async def get_one_prod(self,prod_id: int)->ProductResponseSchema:
        prod= await self.product_repository.get_by_id(prod_id)
        if prod is None:
            raise ProductNotFound(f"Продукт с id: {prod_id} не найден")
        return ProductResponseSchema.model_validate(prod)

    async def create_prod(self,prod_create: ProductCreateSchema)->ProductResponseSchema:

        new_prod = ProductORM(
            name=prod_create.name,
            price=prod_create.price,
            description=prod_create.description,
            image_url=prod_create.image_url
        )
        await self.product_repository.create(new_prod)

        await self.db.commit()
        await self.db.refresh(new_prod)
        return ProductResponseSchema.model_validate(new_prod)

    async def update_prod(
        self,
        prod_id: int,
        prod_update: ProductUpdateSchema,
    )->ProductResponseSchema:

        prod_for_update = await self.product_repository.get_by_id(prod_id)
        if not prod_for_update:
            raise ProductNotFound(f"Продукт с id: {prod_id} не найден")
        if prod_update.name is not None:
            prod_for_update.name = prod_update.name
        if prod_update.price is not None:
            prod_for_update.price = prod_update.price
        if prod_update.description is not None:
            prod_for_update.description = prod_update.description
        if prod_update.image_url is not None:  
            prod_for_update.image_url = prod_update.image_url

        await self.db.commit()
        await self.db.refresh(prod_for_update)
        return ProductResponseSchema.model_validate(prod_for_update)

    async def delete_prod(self, prod_id: int)->None:
        prod_for_del = await self.product_repository.get_by_id(prod_id)
        if prod_for_del is None:
            raise ProductNotFound(f"Продукт с id: {prod_id} не найден")

        await self.product_repository.delete(prod_for_del)
        await self.db.commit()