from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class OrderStatus(Enum):
    IN_PROCCESS = "in_proccess"
    SEND = "send"
    DELIVERED = "delivered"


class Product(BaseModel):
    name: str
    description: str
    price: float
    count: int


class ProductFull(Product):
    id: int


class OrderItem(BaseModel):
    product_id: int
    product_count: int


class Order(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus


class OrderWithItems(Order):
    items: list[OrderItem]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
