from pydantic import BaseModel
from typing import List, Optional


class CheckoutItem(BaseModel):
    product_id: int
    quantity: int


class CheckoutOrder(BaseModel):
    items: List[CheckoutItem]
    # promo_code: Optional[str] = None
    promo_id: Optional[int] = None
