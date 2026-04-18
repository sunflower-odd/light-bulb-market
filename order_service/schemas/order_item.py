from pydantic import BaseModel
from typing import Optional


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: Optional[int] = None


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        from_attributes = True