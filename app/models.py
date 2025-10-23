"""Data models for NoPickles MVP"""

from pydantic import BaseModel
from typing import List, Optional


class MenuItem(BaseModel):
    """Menu item model"""
    id: str
    name: str
    category: str
    price: float
    description: str
    available: bool = True


class OrderItem(BaseModel):
    """Item in an order"""
    menu_item_id: str
    name: str
    quantity: int
    price: float
    special_instructions: Optional[str] = None


class Order(BaseModel):
    """Customer order model"""
    session_id: str
    items: List[OrderItem]
    total: float


class ConversationMessage(BaseModel):
    """Customer message in conversation"""
    session_id: str
    message: str


class OrderResponse(BaseModel):
    """Response to customer with order status"""
    message: str
    order: Order
    suggestions: List[str] = []
