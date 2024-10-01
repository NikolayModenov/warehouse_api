from fastapi import Depends, FastAPI
from typing import List

from sqlalchemy.orm import Session

from docs.response_schemas import (
    create_order_responses, create_product_responses, delete_product_responses,
    order_not_found_responses, product_not_found_responses
)
from docs.messages import description
from sql_app.crud import (
    create_order, create_product, del_product, get_all_orders,
    get_all_products, get_one_order, get_one_product, put_product, update_order
)
from sql_app.database import get_db
from sql_app.schemas import (
    CreateOrderSchema, CreateProductSchema, PatchOrderSchema, ReadOrderSchema,
    ReadProductSchema, UpdateProductSchema
)

APP = FastAPI(
    title="warehouse_api",
    description=description
)

DATABASE_SESSION = Depends(get_db)


@APP.post(
    "/products", response_model=ReadProductSchema, summary="create product",
    responses=create_product_responses
)
def add_product(product: CreateProductSchema, db: Session = DATABASE_SESSION):
    """Create a product with a unique **name**."""
    return create_product(db, product)


@APP.get(
    "/products", response_model=List[ReadProductSchema],
    summary="read products"
)
def get_products(db: Session = DATABASE_SESSION):
    """Get information about all products in stock."""
    return get_all_products(db)


@APP.get(
    "/products/{product_id}", response_model=ReadProductSchema,
    summary="read one product", responses=product_not_found_responses
)
def get_product(product_id: int, db: Session = DATABASE_SESSION):
    """Get information about the product in the warehouse by **id**."""
    return get_one_product(db, product_id)


@APP.put(
    "/products/{product_id}", response_model=ReadProductSchema,
    summary="update product", responses=product_not_found_responses
)
def update_product_info(
        product_id: int, product: UpdateProductSchema,
        db: Session = DATABASE_SESSION
):
    """Change the product's **price** and **description**."""
    return put_product(db, product, product_id)


@APP.delete(
    "/products/{product_id}", summary="delete product",
    responses=delete_product_responses
)
def delete_product(product_id: int, db: Session = DATABASE_SESSION):
    """Delete product."""
    return del_product(db, product_id)


@APP.post(
    "/orders", response_model=ReadOrderSchema, summary="create order",
    responses=create_order_responses
)
def add_order(
        order: CreateOrderSchema, db: Session = DATABASE_SESSION
):
    """
        Create an order with a selection of the order status,
        add products and their quantity in the order.
        You cannot add an item that is not in stock.
        the product of the same name is summed up in one item,
        the quantity of the product
        must not exceed the availability in stock.
    """
    return create_order(db, order)


@APP.get(
    "/orders", response_model=List[ReadOrderSchema], summary="read orders"
)
def get_orders(db: Session = DATABASE_SESSION):
    """Get information about all orders with a list of items in the order."""
    return get_all_orders(db)


@APP.get(
    "/orders/{order_id}", response_model=ReadOrderSchema,
    summary="read one order", responses=order_not_found_responses
)
def get_order(order_id: int, db: Session = DATABASE_SESSION):
    """Get information about the order with a list of products in the order."""
    return get_one_order(order_id, db)


@APP.patch(
    "/orders/{order_id}/status", response_model=ReadOrderSchema,
    summary="change order status", responses=order_not_found_responses
)
def patch_order_status(
        order_id: int, schema: PatchOrderSchema,
        db: Session = DATABASE_SESSION
):
    """Change the order status."""
    return update_order(order_id, schema.status, db)
