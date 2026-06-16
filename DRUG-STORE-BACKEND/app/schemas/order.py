from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class OrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)    
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
class OrderResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)   
    id: UUID
    user_id: UUID
    created_at: datetime
    total_price: float
    status: str
    items: list[OrderItemResponseSchema]
class OrderUpdateSchema(BaseModel):
    status: str