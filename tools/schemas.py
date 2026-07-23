from __future__ import annotations

from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    