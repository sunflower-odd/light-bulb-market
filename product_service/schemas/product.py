from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ProductCreate(BaseModel):
    title: str
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    price: float
    description: Optional[str] = None

class ProductResponse(ProductCreate):
    product_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
