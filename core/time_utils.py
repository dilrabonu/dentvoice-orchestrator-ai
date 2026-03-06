from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class DateResolution:
    """
    Result of resolving natural date tokens like TODAY/TOMORROW.
    """
    iso_date: str  # YYYY-MM-DD
    source: str    # original token (e.g., TODAY)


def resolve_date_token(date_value: str, tz_name: str) -> DateResolution:
    """
    Convert TODAY/TOMORROW tokens to real ISO date based on timezone.
    If already an ISO date, return as-is.

    Args:
        date_value: "TODAY", "TOMORROW" or "YYYY-MM-DD"
        tz_name: IANA timezone name (e.g., "Asia/Tashkent")

    Returns:
        DateResolution(iso_date, source)
    """
    date_value = (date_value or "").strip()

    # Already ISO date
    if len(date_value) == 10 and date_value[4] == "-" and date_value[7] == "-":
        return DateResolution(iso_date=date_value, source="ISO_DATE")

    tz = ZoneInfo(tz_name)
    now_local = datetime.now(tz=tz).date()

    if date_value == "TODAY":
        return DateResolution(iso_date=now_local.isoformat(), source="TODAY")

    if date_value == "TOMORROW":
        return DateResolution(iso_date=(now_local + timedelta(days=1)).isoformat(), source="TOMORROW")

    # Unknown token -> keep as-is (caller decides recovery)
    return DateResolution(iso_date=date_value, source="UNKNOWN")