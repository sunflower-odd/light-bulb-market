from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from order_service.routers import address, delivery, order, order_item, order_promo, review, user
from order_service.db import engine, Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    from order_service import models
    Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(address.router)
app.include_router(delivery.router)
app.include_router(order.router)
app.include_router(order_item.router)
app.include_router(order_promo.router)
app.include_router(review.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)