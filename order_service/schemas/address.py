from pydantic import BaseModel
from typing import Optional


class AddressBase(BaseModel):
    user_id: int
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[int] = None
    apartment: Optional[int] = None
    postal_code: Optional[int] = None


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    user_id: Optional[int] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[int] = None
    apartment: Optional[int] = None
    postal_code: Optional[int] = None


class AddressResponse(AddressBase):
    address_id: int

    class Config:
        from_attributes = True