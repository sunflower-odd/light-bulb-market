from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

import requests

from order_service.db import get_db
from order_service.models.order_item import OrderItem
from order_service.schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemResponse

router = APIRouter(prefix="/order-items", tags=["OrderItems"])

PRODUCT_SERVICE_URL = "http://product_app:8000"

def get_product(product_id: int):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    if response.status_code != 200:
        return None

    return response.json()

@router.get("/", response_model=List[OrderItemResponse])
def get_order_items(db: Session = Depends(get_db)):
    return db.query(OrderItem).all()


@router.post("/", response_model=OrderItemResponse)
def create_order_item(order_item: OrderItemCreate, db: Session = Depends(get_db)):
    db_obj = OrderItem(**order_item.model_dump())

    product = get_product(db_obj.product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/{item_id}", response_model=OrderItemResponse)
def get_order_item_by_id(item_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(OrderItem).filter(OrderItem.id == item_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="OrderItem not found")

    return db_obj


@router.patch("/{item_id}", response_model=OrderItemResponse)
def update_order_item(item_id: int, order_item: OrderItemUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(OrderItem).filter(OrderItem.id == item_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="OrderItem not found")

    update_data = order_item.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)

    return db_obj


@router.delete("/{item_id}")
def delete_order_item(item_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(OrderItem).filter(OrderItem.id == item_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="OrderItem not found")

    db.delete(db_obj)
    db.commit()

    return {"message": "OrderItem deleted successfully"}