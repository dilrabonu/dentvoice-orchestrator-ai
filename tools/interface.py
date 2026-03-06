from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Protocol


@dataclass(frozen=True)
class AvailableSlot:
    date: str   # YYYY-MM-DD
    time: str   # HH:MM


class ClinicTools(Protocol):
    """
    Tool contract for clinic backend.
    In Phase 1 we provide a FakeBackend implementation.
    """

    def get_services(self) -> List[str]:
        ...

    def get_available_slots(self, date: str, service: str) -> List[AvailableSlot]:
        ...

    def create_booking(
        self,
        date: str,
        time: str,
        service: str,
        name: str,
        phone: str,
        idem_key: str,
        doctor: str,
    ) -> dict:
        """
        Must be idempotent by idem_key.
        Must prevent double booking (doctor+date+time unique).
        """
        ...

    def find_customer_by_phone(self, phone: str) -> Optional[dict]:
        ...

    def upsert_customer(self, name: str, phone: str) -> dict:
        ...

    def get_location(self) -> dict:
        ...

    def get_preparation(self, service: str) -> dict:
        ...

    def get_price(self, service: str) -> dict:
        """
        IMPORTANT: OqTabassum policy -> do NOT provide numeric price.
        """
        ...