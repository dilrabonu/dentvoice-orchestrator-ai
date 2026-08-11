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
