from fastapi import APIRouter, Depends,  HTTPException
from typing import List
from sqlalchemy.orm import Session
from product_service.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from product_service.models.product import Product
from product_service.db import get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.add(db_product)
    db.commit()

    return db_product