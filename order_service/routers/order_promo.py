from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import requests

from product_service.db import get_db
from order_service.models.order_promo import OrderPromo
from order_service.schemas.order_promo import OrderPromoCreate, OrderPromoUpdate, OrderPromoResponse

router = APIRouter(prefix="/order-promos", tags=["OrderPromos"])

PRODUCT_SERVICE_URL = "http://product_app:8000"

def get_promo(promo_id: int):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/promos/{promo_id}")

    if response.status_code != 200:
        return None

    return response.json()


@router.get("/", response_model=List[OrderPromoResponse])
def get_order_promos(db: Session = Depends(get_db)):
    return db.query(OrderPromo).all()


@router.post("/", response_model=OrderPromoResponse)
def create_order_promo(order_promo: OrderPromoCreate, db: Session = Depends(get_db)):
    db_obj = OrderPromo(**order_promo.model_dump())

    promo = get_promo(db_obj.promo_id)

    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")


    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/{id}", response_model=OrderPromoResponse)
def get_order_promo_by_id(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(OrderPromo).filter(OrderPromo.id == id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="OrderPromo not found")

    return db_obj


@router.patch("/{id}", response_model=OrderPromoResponse)
def update_order_promo(id: int, order_promo: OrderPromoUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(OrderPromo).filter(OrderPromo.id == id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="OrderPromo not found")

    update_data = order_promo.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)

    return db_obj


@router.delete("/{id}")
def delete_order_promo(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(OrderPromo).filter(OrderPromo.id == id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="OrderPromo not found")

    db.delete(db_obj)
    db.commit()

    return {"message": "OrderPromo deleted successfully"}