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
    In-memory backend for testing then replaces CRM/Booking/Search APIs.
    """
    def __init__(self, default_doctor: str, pricing_mode: str = "NO_PRICE") -> None:
        self.default_doctor = default_doctor
        self.pricing_mode = pricing_mode

        self._customers: Dict[str, dict] = {}
        self._bookings_by_key: Dict[str, dict] = {} 
        self._bookings_unique: Dict[Tuple[str, str, str], _Booking] = {}

    def get_service(self) -> List[str]:
        return ["konsultatsiya", "tish davolash", "tish tozalash"]

    def get_available_slots(self, date: str, service: str) -> List[AvailableSlot]:

        base = ["10:00", "11:30", "14:00", "15:00", "16:30"]
        slots: List[AvailableSlot]  = []
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
    # Idempotency check
        if idem_key in self._bookings_by_key:
            return self._bookings_by_key[idem_key]

    # Double booking protection
        unique = (doctor, date, time)
        if unique in self._bookings_unique:
            resp = {
                "ok": False,
                "error": "SLOT_ALREADY_BOOKED",
                "message": "Kechirasi, bu vaqt band. Boshqa vaqt taklif qilaman.",
            }
            self._bookings_by_key[idem_key] = resp
            return resp

        booking = Booking(
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
        self._bookings_by_phone[idem_key] = resp
        return resp
    
    





    