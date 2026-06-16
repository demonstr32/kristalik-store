import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.cart import CartRepository
from app.repositories.cart_item import CartItemRepository
from app.repositories.prod import ProductRepository
from app.models.cart import CartORM
from app.models.cart_item import CartItemORM
from app.schemas.cart import CartItemSchema, CartItemUpdateSchema, CartItemResponseSchema, CartResponseSchema

class ItemNotFound(Exception):
    """Товара не существует"""
class NotUserCart(Exception):
    """товар в вашей корзине не найден"""
class CartService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
    async def get_cart(self, user_id: str)->CartResponseSchema:
        cart = await self.cart_repository.get_or_create(user_id)
        
        items_orm = await self.cart_item_repository.get_by_cart_id(cart.id)
        tasks = []
        for i in  items_orm:
            product = self.product_repository.get_by_id(i.product_id)
            tasks.append(product)
        result = await asyncio.gather(*tasks) 
        items_response = []
        total_price = 0
        for item, product in zip(items_orm,result):
            
            if product:
                item_response = CartItemResponseSchema(
                        id=item.id,
                        product_id=item.product_id,
                        product_name=product.name,
                        price=product.price,
                        quantity=item.quantity,
                        image_url=product.image_url,
                )
                items_response.append(item_response)
                total_price += product.price * item.quantity
        await self.db.commit()
        return CartResponseSchema(
            id=cart.id,
            user_id=cart.user_id,
            items=items_response,
            total_price=total_price
        )
    async def add_item(self, user_id: str, cart_add: CartItemSchema) -> CartItemResponseSchema:
        if cart_add.quantity<=0:
            raise ValueError("Количество должно быть больше 0")
        product = await self.product_repository.get_by_id(cart_add.product_id)
        if not product:
            raise ValueError("Товар не найден")
        
        cart = await self.cart_repository.get_or_create(user_id)
        existing = await self.cart_item_repository.get_by_cart_and_product(cart.id, cart_add.product_id)
        
        if existing:
            updated_item = await self.cart_item_repository.update_quantity(existing.id, existing.quantity + cart_add.quantity)
            await self.db.commit()
            return CartItemResponseSchema(
                id=updated_item.id,
                product_id=updated_item.product_id,
                product_name=product.name,
                price=product.price,
                quantity=updated_item.quantity,
                image_url=product.image_url,
            )
        else:
            new_item = await self.cart_item_repository.add_item(cart.id, cart_add.product_id, cart_add.quantity)
            await self.db.commit()
            return CartItemResponseSchema(
                id=new_item.id,
                product_id=new_item.product_id,
                product_name=product.name,
                price=product.price,
                quantity=new_item.quantity,
                image_url=product.image_url,
            )

    async def remove_item(self, user_id: str, item_id: int) -> None:
        item = await self.cart_item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFound()
        
        cart = await self.cart_repository.get_by_id(item.cart_id)
        if not cart or cart.user_id != user_id:
            raise PermissionError("Это не ваш товар")
        
        await self.cart_item_repository.remove_item(item_id)
        await self.db.commit()

    async def update_item(self, user_id: str, item_id: int, cart_update: CartItemUpdateSchema) -> CartItemResponseSchema:
        item = await self.cart_item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFound()
        
        cart = await self.cart_repository.get_by_id(item.cart_id)

        
        if cart.user_id != user_id:
            raise NotUserCart()
        
        updated_item = await self.cart_item_repository.update_quantity(item.id, cart_update.quantity)
        product = await self.product_repository.get_by_id(updated_item.product_id)
        await self.db.commit()
        await self.db.refresh(updated_item)
        
        
        return CartItemResponseSchema(
            id=updated_item.id,
            product_id=updated_item.product_id,
            product_name=product.name,
            price=product.price,
            quantity=updated_item.quantity,
            image_url=product.image_url,
        )
    async def clear_cart(self, user_id: str)->None:
        cart = await self.cart_repository.get_or_create(user_id)
        await self.cart_item_repository.clear_cart(cart.id)
        await self.db.commit()