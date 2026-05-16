from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from order_service.db import get_db
from order_service.models.delivery import Delivery
from order_service.schemas.delivery import DeliveryCreate, DeliveryResponse

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])


@router.get("/", response_model=List[DeliveryResponse])
def get_deliveries(db: Session = Depends(get_db)):
    return db.query(Delivery).all()


@router.post("/", response_model=DeliveryResponse)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = Delivery(**delivery.model_dump())

    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)

    return db_delivery


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery_by_id(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(Delivery).filter(
        Delivery.delivery_id == delivery_id
    ).first()

    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return db_delivery


@router.patch("/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(
    delivery_id: int,
    delivery: DeliveryCreate,
    db: Session = Depends(get_db)
):
    db_delivery = db.query(Delivery).filter(
        Delivery.delivery_id == delivery_id
    ).first()

    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    update_data = delivery.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_delivery, key, value)

    db.commit()
    db.refresh(db_delivery)

    return db_delivery

@router.delete("/{delivery_id}")
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(Delivery).filter(
        Delivery.delivery_id == delivery_id
    ).first()

    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    db.delete(db_delivery)
    db.commit()

    return {"message": "Delivery deleted successfully"}