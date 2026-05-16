import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from core.auth import get_current_user

app = FastAPI()
print("STARTED")
BASE_PRODUCT_URL = "http://product_app:8000"
BASE_ORDER_URL = "http://order_app:8001"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def safe_request(method: str, url: str, **kwargs):
    try:
        response = requests.request(method, url, timeout=5, **kwargs)
        response.raise_for_status()
        return response.json()

    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response else 502

        raise HTTPException(
            status_code=status_code,
            detail=e.response.text if e.response else "Upstream HTTP error"
        )

    except requests.RequestException as e:
        # network / timeout / dns / connection refused
        raise HTTPException(
            status_code=503,
            detail=f"Upstream service unavailable: {str(e)}"
        )

@app.get("/products")
def get_products(
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
):
    params = {
        k: v for k, v in {
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "search": search,
        }.items()
        if v is not None
    }

    return safe_request(
        "GET",
        f"{BASE_PRODUCT_URL}/products",
        params=params
    )


@app.post("/products")
def create_product(product: dict):
    return safe_request(
        "POST",
        f"{BASE_PRODUCT_URL}/products",
        json=product
    )


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    return safe_request(
        "GET",
        f"{BASE_PRODUCT_URL}/products/{product_id}"
    )


@app.patch("/products/{product_id}")
def update_product(product_id: int, product: dict):
    return safe_request(
        "PATCH",
        f"{BASE_PRODUCT_URL}/products/{product_id}",
        json=product
    )

@app.get("/categories")
def get_categories():
    return safe_request(
        "GET",
        f"{BASE_PRODUCT_URL}/categories",
    )

@app.get("/orders")
def get_orders(user: dict = Depends(get_current_user)):

    headers = {
        "X-User-ID": str(user["user_id"])
    }

    return safe_request(
        "GET",
        f"{BASE_ORDER_URL}/orders",
        headers=headers
    )

@app.patch("/orders/{order_id}")
def update_order(order_id: int, order: dict):
    return safe_request(
        "PATCH",
        f"{BASE_ORDER_URL}/products/{order_id}",
        json=order
    )
