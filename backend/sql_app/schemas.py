from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from sql_app.models import StatusEnum


class CreateProductSchema(BaseModel):
    name: str = Field(
        min_length=1, max_length=200, description="product name"
    )
    description: str = Field(max_length=500, description="product description")
    price: float = Field(gt=0, description="product price")
    quantity_in_stock: int = Field(
        ge=0, description="quantity of product in stock"
    )


class UpdateProductSchema(BaseModel):
    description: Optional[str] = Field(
        max_length=500, description="product description", default=None
    )
    price: Optional[float] = Field(
        ge=0, description="product price", default=None
    )


class CreateOrderItemSchema(BaseModel):
    product: str = Field(
        min_length=1, max_length=200, description="product name"
    )
    item_quantity: int = Field(
        gt=0, description="quantity of product in stock"
    )


class CreateOrderSchema(BaseModel):
    status: StatusEnum = Field(description="order status")
    items: List[CreateOrderItemSchema] = Field(
        description="list of items in the order"
    )


class ReadOrderItemSchema(BaseModel):
    id: int = Field(description="item id")
    product: str = Field(
        min_length=1, max_length=200, description="item name"
    )
    item_quantity: int = Field(
        gt=0, description="the quantity of the item in the order"
    )


class ReadOrderSchema(BaseModel):
    id: int = Field(description="order id")
    created_at: datetime = Field(description="order creation date")
    status: StatusEnum = Field(description="order status")
    items: List[ReadOrderItemSchema] = Field(
        description="list of items in the order"
    )


class PatchOrderSchema(BaseModel):
    status: StatusEnum = Field(description="order status")

class ReadProductSchema(CreateProductSchema):
    id: int = Field(description="product id")
