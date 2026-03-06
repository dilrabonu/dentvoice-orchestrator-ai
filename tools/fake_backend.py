from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from tools.interfaces import AvailableSlot


@dataclass
class _Booking:
    doctor: str
    date: str
    time: str
    service: str
    name: str
    phone: str
    idem_key: str


class FakeClinicBackend:
    """
    In-memory backend for Phase 1.
    Replaces CRM/Booking/Search APIs.
    """

    def __init__(self, default_doctor: str, pricing_mode: str = "NO_PRICE") -> None:
        self._default_doctor = default_doctor
        self._pricing_mode = pricing_mode

        self._customers: Dict[str, dict] = {}  # phone -> customer
        self._bookings_by_key: Dict[str, dict] = {}  # idem_key -> response
        self._bookings_unique: Dict[Tuple[str, str, str], _Booking] = {}  # (doctor,date,time) -> booking

    def get_services(self) -> List[str]:
        return ["konsultatsiya", "tish davolash", "tish tozalash"]

    def get_available_slots(self, date: str, service: str) -> List[AvailableSlot]:
        # In real backend: query schedule table.
        # Here: return a stable set and remove already booked times.
        base = ["10:00", "11:30", "15:00", "16:30"]
        slots: List[AvailableSlot] = []
        for t in base:
            key = (self._default_doctor, date, t)
            if key not in self._bookings_unique:
                slots.append(AvailableSlot(date=date, time=t))
        return slots

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
        # 1) Idempotency check
        if idem_key in self._bookings_by_key:
            return self._bookings_by_key[idem_key]

        # 2) Double booking protection
        unique = (doctor, date, time)
        if unique in self._bookings_unique:
            resp = {
                "ok": False,
                "error": "SLOT_ALREADY_BOOKED",
                "message": "Kechirasiz, bu vaqt band. Boshqa vaqt taklif qilaman.",
            }
            self._bookings_by_key[idem_key] = resp
            return resp

        booking = _Booking(
            doctor=doctor,
            date=date,
            time=time,
            service=service,
            name=name,
            phone=phone,
            idem_key=idem_key,
        )
        self._bookings_unique[unique] = booking
        resp = {
            "ok": True,
            "booking_id": f"bk_{doctor}_{date}_{time}".replace(":", ""),
            "doctor": doctor,
            "date": date,
            "time": time,
            "service": service,
            "name": name,
            "phone": phone,
        }
        self._bookings_by_key[idem_key] = resp
        return resp

    def find_customer_by_phone(self, phone: str) -> Optional[dict]:
        return self._customers.get(phone)

    def upsert_customer(self, name: str, phone: str) -> dict:
        self._customers[phone] = {"name": name, "phone": phone}
        return self._customers[phone]

    def get_location(self) -> dict:
        # Replace with real address later.
        return {
            "address": "OqTabassum stomatologiya klinikasi (manzil keyin real bilan to‘ldiriladi)",
            "landmark": "Mo‘ljal: markaziy ko‘cha yaqinida",
        }

    def get_preparation(self, service: str) -> dict:
        # Keep it simple and safe.
        return {
            "service": service,
            "instructions": [
                "Ko‘rikdan oldin 10 daqiqa ertaroq keling.",
                "Agar og‘riq bo‘lsa, shifokorga albatta ayting.",
            ],
        }

    def get_price(self, service: str) -> dict:
        # POLICY: never disclose numeric price
        return {
            "service": service,
            "pricing_policy": "Narx ko‘rikdan keyin aniq bo‘ladi.",
            "can_estimate": False,
        }