# src/models/__init__.py
from models.role import Role
from models.user import User
from models.categories import Category
from models.status import Status
from models.room import Room
from models.payments import PaymentMethod
from models.reservation import Reservation
from models.lodging import Lodging

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