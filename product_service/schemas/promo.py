from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PromoUpdate(BaseModel):
    description: Optional[str] = None
    discount_percent: int
    start_date: datetime
    end_date: datetime


class PromoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    discount_percent: int
    start_date: datetime
    end_date: datetime

class PromoResponse(PromoCreate):
    promo_id: int
    discount_percent: int
    created_at: datetime

    class Config:
        from_attributes = True
