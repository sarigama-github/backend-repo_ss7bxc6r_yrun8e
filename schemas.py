"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

# Dentistry app schemas

class Appointment(BaseModel):
    """
    Dental appointments booked by visitors
    Collection name: "appointment"
    """
    name: str = Field(..., min_length=2, max_length=100, description="Patient full name")
    email: EmailStr = Field(..., description="Patient email")
    phone: str = Field(..., min_length=7, max_length=20, description="Contact phone number")
    service: str = Field(..., description="Requested service (e.g., Cleaning, Checkup)")
    appointment_date: date = Field(..., description="Preferred appointment date")
    time_slot: str = Field(..., description="Preferred time window, e.g., 10:00 AM")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")

class Consultation(BaseModel):
    """
    Virtual/phone consultation requests
    Collection name: "consultation"
    """
    name: str = Field(..., min_length=2, max_length=100, description="Visitor name")
    email: EmailStr = Field(..., description="Visitor email")
    phone: Optional[str] = Field(None, min_length=7, max_length=20, description="Phone number")
    message: str = Field(..., min_length=10, max_length=1000, description="What would you like to discuss?")
    preferred_date: Optional[date] = Field(None, description="Optional preferred date")

# Example schemas retained for reference (not used by app but kept for viewer compatibility)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
