# src/models/__init__.py
from src.models.role import Role
from src.models.user import User
from src.models.categories import Category
from src.models.status import Status
from src.models.room import Room
from src.models.payments import PaymentMethod
from src.models.reservation import Reservation
from src.models.lodging import Lodging

# Opcional: define qué se expone al hacer import *
__all__ = [
    "Role", 
    "User", 
    "Category", 
    "Status", 
    "PaymentMethod", 
    "Room",
    "Reservation",
    "Lodging"
    ]