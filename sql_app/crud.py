from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import desc, exists, update
from sqlalchemy.orm import Session

from models import Order, Product
from schemas import CreateOrderSchema, CreateProductSchema, UpdateProductSchema
from services import (
    get_item_objects_and_total_stock_balance, prepare_order_to_response,
    validate_and_get_order_items
)


def create_product(db: Session, product: CreateProductSchema):
    if db.query(exists().where(Product.name == product.name)).scalar():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"A product named {product.name} already exists."
        )
    db_product = Product(
        name=product.name, description=product.description,
        price=product.price, quantity_in_stock=product.quantity_in_stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_all_products(db: Session):
    return db.query(Product).all()


def get_one_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def put_product(db: Session, product: UpdateProductSchema, product_id: int):
    db_product = db.get(Product, product_id)
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    if not product.description:
        db_product.description = product.description
    if not product.price:
        db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return db_product


def del_product(db: Session, product_id: int):
    db_product = db.get(Product, product_id)
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    db.delete(db_product)
    db.commit()
    return {"message": "product successfully delete"}


def create_order(db: Session, order: CreateOrderSchema):
    order_items = validate_and_get_order_items(db, order.items)
    last_order = db.query(Order).order_by(desc(Order.id)).first()
    if not last_order:
        expected_order_id = 1
    else:
        expected_order_id = last_order.id + 1
    new_order = Order(status=order.status)
    db.add(new_order)
    db.flush()
    if expected_order_id != db.query(Order).order_by(
            desc(Order.id)
    ).first().id:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An error occurred when creating a record in the database."
        )
    item_objects, total_stock_balance = (
        get_item_objects_and_total_stock_balance(
            order_items, expected_order_id, db
        )
    )
    db.bulk_save_objects(item_objects)
    db.execute(update(Product), total_stock_balance)
    db.commit()
    db.refresh(new_order)
    return prepare_order_to_response(new_order)


def get_all_orders(db: Session):
    response = []
    for db_order in db.query(Order).all():
        response.append(prepare_order_to_response(db_order))
    return response


def get_one_order(order_id: int, db: Session):
    db_order = db.get(Order, order_id)
    return prepare_order_to_response(db_order)


def update_order(order_id, changing_status, db):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    db_order.status = changing_status
    db.commit()
    db.refresh(db_order)
    return prepare_order_to_response(db_order)
