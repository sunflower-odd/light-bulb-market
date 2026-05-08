from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from order_service.db import get_db
from order_service.models.user import User
from order_service.schemas.user import UserCreate, UserUpdate, UserResponse
from order_service.auth import create_access_token

from fastapi import Depends

router = APIRouter(prefix="/users", tags=["Users"])

router_auth = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_obj = User(**user.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(User).filter(User.user_id == user_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return db_obj


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(User).filter(User.user_id == user_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)

    return db_obj


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(User).filter(User.user_id == user_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_obj)
    db.commit()

    return {"message": "User deleted successfully"}


@router_auth.post("/login")
def login(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token({
        "user_id": user.user_id,
        "email": user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
#
# @router.post("/checkout")
# def checkout(
#     order: CheckoutOrder,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     if not user:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#
#     user_id = user["user_id"]
#
#     # 1. создаём заказ (SQLAlchemy model!)
#     db_order = Order(
#         user_id=user_id,
#         status="NEW"
#     )
#
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)
#
#     order_id = db_order.order_id
#
#     total = 0
#
#     # 2. items
#     for item in order.items:
#
#         product = get_product(item.product_id)
#         if not product:
#             raise HTTPException(status_code=404, detail="Product not found")
#
#         price = product["price"]
#         total += price * item.quantity
#
#         db_item = OrderItem(
#             order_id=order_id,
#             product_id=item.product_id,
#             quantity=item.quantity,
#             price=price
#         )
#
#         db.add(db_item)
#
#     discount = 0
#
#     # 3. promo
#     if order.promo_id:
#         promo = get_promo(order.promo_id)
#
#         if promo:
#             discount = promo["discount_percent"]
#
#             db_promo = OrderPromo(
#                 order_id=order_id,
#                 promo_id=order.promo_id,
#                 discount_percent=discount
#             )
#
#             db.add(db_promo)
#
#     db.commit()
#
#     final_total = total - (total * discount / 100)
#
#     return {
#         "order_id": order_id,
#         "total": total,
#         "discount": discount,
#         "final_total": final_total
#     }