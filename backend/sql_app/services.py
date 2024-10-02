from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func

from sql_app.models import OrderItem, Product


def validate_product_availability(db, product_name):
    count_products = db.query(func.count(Product.id).filter(
        Product.name == product_name
    )).scalar()
    if count_products == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Product with name {product_name} not found"
        )
    if count_products != 1:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=(
                "The database returned a product "
                f"with the name {product_name} "
                f"in the amount of {count_products} pieces. "
                "Only one entry should have been returned."
            )
        )


def validate_and_get_order_items(db, items):
    order_items = {}
    for item in items:
        product_name = item.product
        item_quantity = item.item_quantity
        validate_product_availability(db, product_name)
        product_in_db = db.query(Product).filter(
            Product.name == product_name
        ).first()
        if product_name not in order_items:
            order_items[product_name] = item_quantity
        else:
            order_items[product_name] += item_quantity
        if product_in_db.quantity_in_stock < order_items[product_name]:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    "The quantity of the product in the order exceeds its "
                    "availability in stock. "
                    f"Quantity {product_name} in order: "
                    f"{order_items[product_name]}; "
                    f"Quantity {product_name} in stock: "
                    f"{product_in_db.quantity_in_stock}."
                )
            )
    if not order_items:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="The order is empty. Add items to the order."
        )
    return order_items


def get_item_objects_and_total_stock_balance(order_items, db_order_id, db):
    item_objects = []
    total_stock_balance = []
    for product_name in order_items:
        item_quantity = order_items[product_name]
        db_product = db.query(Product).filter(
            Product.name == product_name
        ).first()
        item_objects.append(OrderItem(
            order_id=db_order_id, product_id=db_product.id,
            item_quantity=item_quantity
        ))
        stock_balance = db_product.quantity_in_stock - item_quantity
        total_stock_balance.append({
            "id": db_product.id, "quantity_in_stock": stock_balance
        })
    return item_objects, total_stock_balance


def prepare_order_to_response(db_order):
    items = []
    for db_item in db_order.items:
        items.append({
            "id": db_item.id, "product": db_item.product.name,
            "item_quantity": db_item.item_quantity
        })
    return {
        "id": db_order.id, "created_at": db_order.created_at,
        "status": db_order.status, "items": items
    }
