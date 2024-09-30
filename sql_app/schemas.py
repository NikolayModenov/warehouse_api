from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from models import StatusEnum


class CreateProductSchema(BaseModel):
    name: str = Field(
        min_length=1, max_length=200, description="Название продукта"
    )
    description: str = Field(max_length=500, description="Описание продукта")
    price: float = Field(gt=0, description="Цена продукта")
    quantity_in_stock: int = Field(
        ge=0, description="Количество продукта на складе"
    )


class UpdateProductSchema(BaseModel):
    description: Optional[str] = Field(
        max_length=500, description="Описание продукта", default=None
    )
    price: Optional[float] = Field(
        ge=0, description="Цена продукта", default=None
    )


class CreateOrderItemSchema(BaseModel):
    product: str = Field(
        min_length=1, max_length=200, description="Название товара"
    )
    item_quantity: int = Field(
        gt=0, description="Количество товара в заказе"
    )


class CreateOrderSchema(BaseModel):
    status: StatusEnum = Field(description="Статус заказа")
    items: List[CreateOrderItemSchema] = Field(description="Статус заказа")


class ReadOrderItemSchema(BaseModel):
    id: int = Field(description="Идентификатор товара")
    product: str = Field(
        min_length=1, max_length=200, description="Название товара"
    )
    item_quantity: int = Field(
        gt=0, description="Количество товара в заказе"
    )


class ReadOrderSchema(BaseModel):
    id: int = Field(description="Идентификатор заказа")
    created_at: datetime = Field(description="Дата создания")
    status: StatusEnum = Field(description="Статус заказа")
    items: List[ReadOrderItemSchema] = Field(description="Статус заказа")


class PatchOrderSchema(BaseModel):
    status: StatusEnum = Field(description="Статус заказа")
