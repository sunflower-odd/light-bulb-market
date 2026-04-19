from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import requests

from order_service.db import get_db
from order_service.models.review import Review
from order_service.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])

PRODUCT_SERVICE_URL = "http://product_app:8000"

def get_product(product_id: int):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    if response.status_code != 200:
        return None

    return response.json()

@router.get("/", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.model_dump())

    product = get_product(db_review.product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Promo not found")


    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.review_id == review_id).first()

    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    return db_review


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db)
):
    db_review = db.query(Review).filter(Review.review_id == review_id).first()

    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    update_data = review.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)

    return db_review


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.review_id == review_id).first()

    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()

    return {"message": "Review deleted successfully"}