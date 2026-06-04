from uuid import UUID
from pydantic import BaseModel, ConfigDict

class CartItemSchema(BaseModel):
    product_id: int
    quantity: int
class CartItemUpdateSchema(BaseModel):
    quantity: int
class CartItemResponseSchema(BaseModel):
    model_config =ConfigDict(from_attributes=True)
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
class CartResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    items: list[CartItemResponseSchema]
    total_price: float