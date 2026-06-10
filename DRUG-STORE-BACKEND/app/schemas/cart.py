from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class CartItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Количество должно быть больше 0")
class CartItemUpdateSchema(BaseModel):
    quantity: int
class CartItemResponseSchema(BaseModel):
    model_config =ConfigDict(from_attributes=True)
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    image_url: str | None = None
class CartResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    items: list[CartItemResponseSchema]
    total_price: float