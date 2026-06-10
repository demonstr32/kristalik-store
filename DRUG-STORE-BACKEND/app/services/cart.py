from sqlalchemy.orm import Session
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
    def __init__(self, db: Session) -> None:
        self.db = db
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
    def get_cart(self, user_id: str)->CartResponseSchema:
        cart = self.cart_repository.get_or_create(user_id)
        items_orm = self.cart_item_repository.get_by_cart_id(cart.id)
        items_response = []
        total_price = 0
        for item in items_orm:
            product = self.product_repository.get_by_id(item.product_id)
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
        return CartResponseSchema(
            id=cart.id,
            user_id=cart.user_id,
            items=items_response,
            total_price=total_price
        )
    def add_item(self, user_id: str, cart_add: CartItemSchema) -> CartItemResponseSchema:
        if cart_add.quantity<=0:
            raise ValueError("Количество должно быть больше 0")
        product = self.product_repository.get_by_id(cart_add.product_id)
        if not product:
            raise ValueError("Товар не найден")
        
        cart = self.cart_repository.get_or_create(user_id)
        existing = self.cart_item_repository.get_by_cart_and_product(cart.id, cart_add.product_id)
        
        if existing:
            updated_item = self.cart_item_repository.update_quantity(existing.id, existing.quantity + cart_add.quantity)
            self.db.commit()
            self.db.refresh(updated_item)
            return CartItemResponseSchema(
                id=updated_item.id,
                product_id=updated_item.product_id,
                product_name=product.name,
                price=product.price,
                quantity=updated_item.quantity,
                image_url=product.image_url,
            )
        else:
            new_item = self.cart_item_repository.add_item(cart.id, cart_add.product_id, cart_add.quantity)
            self.db.commit()
            self.db.refresh(new_item)
            return CartItemResponseSchema(
                id=new_item.id,
                product_id=new_item.product_id,
                product_name=product.name,
                price=product.price,
                quantity=new_item.quantity,
                image_url=product.image_url,
            )

    def remove_item(self, user_id: str, item_id: int) -> None:
        item = self.cart_item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFound()
        
        cart = self.cart_repository.get_by_id(item.cart_id)
        if not cart or cart.user_id != user_id:
            raise PermissionError("Это не ваш товар")
        
        self.cart_item_repository.remove_item(item_id)
        self.db.commit()

    def update_item(self, user_id: str, item_id: int, cart_update: CartItemUpdateSchema) -> CartItemResponseSchema:
        item = self.cart_item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFound()
        
        cart = self.cart_repository.get_by_id(item.cart_id)

        
        if cart.user_id != user_id:
            raise NotUserCart()
        
        updated_item = self.cart_item_repository.update_quantity(item.id, cart_update.quantity)
        self.db.commit()
        self.db.refresh(updated_item)
        
        product = self.product_repository.get_by_id(updated_item.product_id)
        return CartItemResponseSchema(
            id=updated_item.id,
            product_id=updated_item.product_id,
            product_name=product.name,
            price=product.price,
            quantity=updated_item.quantity,
            image_url=product.image_url,
        )
    def clear_cart(self, user_id: str)->None:
        cart = self.cart_repository.get_or_create(user_id)
        self.cart_item_repository.clear_cart(cart.id)
        self.db.commit()