from fastapi import FastAPI
from routers import products, users

app = FastAPI(title="Ejemplo del ejercicio 8")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])


@app.get("/")
def home():
    return {"message": "API REST with routers"}
