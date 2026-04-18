from fastapi import FastAPI

from order_service.routers import address, delivery, order, order_item, order_promo, reviews
from order_service.db import engine, Base
from order_service import models


app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(address.router)
app.include_router(delivery.router)
app.include_router(order.router)
app.include_router(order_item.router)
app.include_router(order_promo.router)
app.include_router(reviews.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)