from fastapi import Depends, FastAPI
from typing import List

from sqlalchemy.orm import Session

from sql_app.crud import (
    create_order, create_product, del_product, get_all_orders,
    get_all_products, get_one_order, get_one_product, put_product, update_order
)
from sql_app.database import get_db
from sql_app.schemas import (
    CreateOrderSchema, CreateProductSchema, PatchOrderSchema, ReadOrderSchema,
    UpdateProductSchema
)

APP = FastAPI()

DATABASE_SESSION = Depends(get_db)


@APP.post("/products")
def add_product(product: CreateProductSchema, db: Session = DATABASE_SESSION):
    return create_product(db, product)


@APP.get("/products")
def get_products(db: Session = DATABASE_SESSION):
    return get_all_products(db)


@APP.get("/products/{product_id}")
def get_product(product_id: int, db: Session = DATABASE_SESSION):
    return get_one_product(db, product_id)


@APP.put("/products/{product_id}")
def update_product_info(
        product_id: int, product: UpdateProductSchema,
        db: Session = DATABASE_SESSION
):
    return put_product(db, product, product_id)


@APP.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = DATABASE_SESSION):
    return del_product(db, product_id)


@APP.post("/orders", response_model=ReadOrderSchema)
def add_order(
        order: CreateOrderSchema, db: Session = DATABASE_SESSION
):
    return create_order(db, order)


@APP.get("/orders", response_model=List[ReadOrderSchema])
def get_orders(db: Session = DATABASE_SESSION):
    return get_all_orders(db)


@APP.get("/orders/{order_id}", response_model=ReadOrderSchema)
def get_order(order_id: int, db: Session = DATABASE_SESSION):
    return get_one_order(order_id, db)


@APP.patch("/orders/{order_id}/status", response_model=ReadOrderSchema)
def patch_order_status(
        order_id: int, schema: PatchOrderSchema,
        db: Session = DATABASE_SESSION
):
    return update_order(order_id, schema.status, db)
