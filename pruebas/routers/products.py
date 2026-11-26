from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class Product(BaseModel):
    id: int
    name: str
    price: float = Field(gt=0)


products_list = [
    Product(id=1, name="t-shirt", price=14.99),
    Product(id=2, name="bottle", price=1.99),
    Product(id=3, name="keyboard", price=39.95),
]


def search_product(id: int):
    for product in products_list:
        if product.id == id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@router.get("")
def get_products():
    return products_list


@router.get("/{id}")
def get_product_by_id(id: int):
    return search_product(id)
