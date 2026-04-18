from pydantic import BaseModel
from datetime import datetime


class PaymentBase(BaseModel):
    order_id: int
    payment_type: str
    payment_system: str
    transaction_id: str
    payment_amount_rub: int
    payment_datetime: datetime
    status: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    order_id: int | None = None
    payment_type: str | None = None
    payment_system: str | None = None
    transaction_id: str | None = None
    payment_amount_rub: int | None = None
    payment_datetime: datetime | None = None
    status: str | None = None


class PaymentResponse(PaymentBase):
    payment_id: int

    class Config:
        from_attributes = True