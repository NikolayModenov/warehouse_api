import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class StatusEnum(enum.Enum):
    in_progress = "В обработке"
    sent = "Отправлен"
    delivered = "Доставлен"


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    status = Column(Enum(StatusEnum), nullable=False)
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan",
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="items")
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="items")
    item_quantity = Column(Integer, nullable=False)
