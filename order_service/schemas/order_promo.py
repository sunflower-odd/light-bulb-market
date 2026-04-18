from pydantic import BaseModel

class OrderPromo(BaseModel):
    id: int
    order_id: int
    promo_id: int
