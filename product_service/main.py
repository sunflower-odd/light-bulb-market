from fastapi import FastAPI

from product_service.routers import product, category, promo
from product_service.db import engine, Base
from product_service import models


app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(product.router)
app.include_router(category.router)
app.include_router(promo.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)