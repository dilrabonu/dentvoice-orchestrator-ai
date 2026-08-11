"""Postgres data models (Phase 6 target).

Not wired into the app yet - Phase 1 uses the in-memory fake DB in
tools/booking_tools.py. Defining the schema now so Phase 6 is a swap,
not a redesign.
"""

from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass 

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(String, index=True)
    name : Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("tenant_id", "doctor_id", "date", "time", name="uq_doctor_slot"),
    )

    id : Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(String, index=True)
    doctor_id: Mapped[str] = mapped_column(String, index=True)
    service: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String, index=True)
    time: Mapped[str] = mapped_column(String, index=True)
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(String, default="confirmed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ToolAuditLog(Base):
    __tablename__ = "tool_audit_logs"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(String, index=True)
    call_id: Mapped[str] = mapped_column(String, index=True)
    idempotency_key: Mapped[str] = mapped_column(String, unique=True)
    tool_name: Mapped[str] = mapped_column(String)
    user_id: Mapped[str] = mapped_column(String)
    user_input: Mapped[str] = mapped_column(String)
    assistant_response: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)