from pydantic import BaseModel
from datetime import datetime

class Delivery(BaseModel):
    delivery_id: int
    order_id: int
    address_id: int
    courier_service: str
    tracking_number: str
    delivery_date: datetime
    delivery_status: str

class DeliveryCreate(BaseModel):
    order_id: int
    address_id: int
    courier_service: str
    tracking_number: str
    delivery_date: datetime
    delivery_status: str

class DeliveryResponse(DeliveryCreate):
    delivery_id: int

    class Config:
        from_attributes = True

