from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from product_service.db import get_db
from product_service.models.category import Category
from product_service.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.model_dump())

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)

    return db_category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()

    return {"message": "Category deleted successfully"}