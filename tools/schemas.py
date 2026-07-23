from __future__ import annotations

from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    phone: str

class Booking(BaseModel):
    booking_id: str
    doctor: str
    service: str
    date: str
    time: str
    customer_name: str
    customer_phone: str
    status: str = "confirmed"

class HandoffRequest(BaseModel):
    reason: str
    summary: dict
