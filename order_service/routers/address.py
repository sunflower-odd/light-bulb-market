from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from product_service.db import get_db
from order_service.models.address import Address
from order_service.schemas.address import AddressCreate, AddressUpdate, AddressResponse

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/", response_model=List[AddressResponse])
def get_addresses(db: Session = Depends(get_db)):
    return db.query(Address).all()


@router.post("/", response_model=AddressResponse)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    db_obj = Address(**address.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/{address_id}", response_model=AddressResponse)
def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Address).filter(Address.address_id == address_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Address not found")

    return db_obj


@router.patch("/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(Address).filter(Address.address_id == address_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Address not found")

    update_data = address.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)

    return db_obj


@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Address).filter(Address.address_id == address_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(db_obj)
    db.commit()

    return {"message": "Address deleted successfully"}