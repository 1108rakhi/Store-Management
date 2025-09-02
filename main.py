from fastapi import FastAPI
from routers import product_router, customer_router, order_router, report_router  

app = FastAPI()
app.include_router(product_router.router)
app.include_router(customer_router.router)
app.include_router(order_router.router)
app.include_router(report_router.router)


@app.get("/")
def home():
    return {"message": "Store Management System is alive 🛒"}
