from pydantic import BaseModel


class OrderPromoBase(BaseModel):
    order_id: int
    promo_id: int


class OrderPromoCreate(OrderPromoBase):
    pass


class OrderPromoUpdate(BaseModel):
    order_id: int | None = None
    promo_id: int | None = None


class OrderPromoResponse(OrderPromoBase):
    id: int

    class Config:
        from_attributes = True