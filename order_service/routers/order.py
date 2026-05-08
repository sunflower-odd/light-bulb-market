from fastapi import APIRouter, Depends, HTTPException

from order_service.schemas.order import OrderCreate, OrderUpdate, OrderResponse

from sqlalchemy.orm import Session
from product_service.db import get_db

from order_service.auth import get_current_user
from order_service.schemas.checkout import CheckoutOrder
from order_service.models.order import Order
from order_service.models.order_item import OrderItem
from order_service.models.order_promo import OrderPromo
from order_service.routers.order_promo import get_promo
from order_service.routers.order_item import get_product


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/")
def get_user_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    print("USER FROM AUTH:", user)
    orders = db.query(Order).filter(Order.user_id == user["user_id"]).all()
    return orders


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return db_order


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(db_order)
    db.commit()

    return {"message": "Order deleted successfully"}


@router.post("/checkout")
def checkout(
    order: CheckoutOrder,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = user["user_id"]

    total = 0
    discount = 0

    # 1. items + считаем total
    for item in order.items:

        product = get_product(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        price = product["price"]
        total += price * item.quantity

    # 2. promo
    if order.promo_id is not None:
        promo = get_promo(order.promo_id)

        if promo:
            discount = promo["discount_percent"]

    # 3. final total
    final_total = total - (total * discount / 100)

    # 4. создаём заказ уже с готовыми данными
    db_order = Order(
        user_id=user_id,
        status="NEW",
        amount_rub=final_total
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    order_id = db_order.order_id

    # 5. сохраняем items
    for item in order.items:

        product = get_product(item.product_id)

        db_item = OrderItem(
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product["price"]
        )

        db.add(db_item)

    # 6. promo запись
    if order.promo_id is not None and discount > 0:

        db_promo = OrderPromo(
            order_id=order_id,
            promo_id=order.promo_id,
            discount_percent=discount
        )

        db.add(db_promo)

    db.commit()

    return {
        "order_id": order_id,
        "total": total,
        "discount": discount,
        "final_total": final_total
    }