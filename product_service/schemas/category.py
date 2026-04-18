from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CategoryCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryCreate):
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True
