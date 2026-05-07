from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from datetime import datetime

from product_service.db import get_db
from product_service.models.promo import Promo
from product_service.schemas.promo import PromoCreate, PromoUpdate, PromoResponse

router = APIRouter(prefix="/promos", tags=["Promos"])


@router.get("/", response_model=List[PromoResponse])
def get_promos(db: Session = Depends(get_db)):
    return db.query(Promo).all()


@router.get("/{promo_id}", response_model=PromoResponse)
def get_promo(promo_id: int, db: Session = Depends(get_db)):
    promo = db.query(Promo).filter(Promo.promo_id == promo_id).first()

    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")

    return promo


@router.get("/check/{title}")
def check_promo(
    title: str,
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()

    promo = (
        db.query(Promo)
        .filter(
            Promo.title == title,
            Promo.start_date <= now,
            Promo.end_date >= now
        )
        .first()
    )

    if not promo:
        raise HTTPException(
            status_code=404,
            detail="Promo not found or expired"
        )

    return {
        "title": promo.title,
        "discount_percent": promo.discount_percent
    }

@router.post("/", response_model=PromoResponse)
def create_promo(promo: PromoCreate, db: Session = Depends(get_db)):
    db_promo = Promo(**promo.model_dump())

    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)

    return db_promo


@router.patch("/{promo_id}", response_model=PromoResponse)
def update_promo(promo_id: int, promo: PromoUpdate, db: Session = Depends(get_db)):
    db_promo = db.query(Promo).filter(Promo.promo_id == promo_id).first()

    if not db_promo:
        raise HTTPException(status_code=404, detail="Promo not found")

    update_data = promo.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_promo, key, value)

    db.commit()
    db.refresh(db_promo)

    return db_promo


@router.delete("/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    db_promo = db.query(Promo).filter(Promo.promo_id == promo_id).first()

    if not db_promo:
        raise HTTPException(status_code=404, detail="Promo not found")

    db.delete(db_promo)
    db.commit()

    return {"message": "Promo deleted successfully"}
