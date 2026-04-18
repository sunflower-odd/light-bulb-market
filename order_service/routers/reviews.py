from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from product_service.db import get_db
from product_service.models.review import Review
from product_service.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.model_dump())
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