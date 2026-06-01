from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProductCreateSchema(BaseModel):
    name: str
    price: float
    description: str | None=None
    image_url: str | None=None
class ProductUpdateSchema(BaseModel):
    name: str | None=None
    price: float | None=None
    description: str | None=None
    image_url: str | None=None
class ProductResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str 
    price: float 
    description: str | None
    image_url: str  | None
    created_at: datetime
    updated_at: datetime