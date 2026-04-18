from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PromoUpdate(BaseModel):
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime


class PromoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime

class PromoResponse(PromoCreate):
    promo_id: int
    created_at: datetime

    class Config:
        from_attributes = True
