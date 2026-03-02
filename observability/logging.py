from __future__ import annotations

import logging

from typing import Any, Dict, Optional

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Create a consistent logger across services.

    Args:
    name: Logger name
    level: Log level string (INFO, DEBUG, etc)

    Returns:
    Configured logger.
    """

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def kv(**fields: Any) -> str:
    """
    Convert key/value fields into a compact log suffix.
    Example: kv(call_is="123", state="Greeting") -> "call_id=123, state=Greeting"
    """
    safe: Dict[str, Any] = {k: v for k, v in fields.items() if v is not None}
    return " ".join(f"{k}={v}" for k, v in safe.items())

def mask_phone(phone: str, keep_last: int = 3) -> str:
    """
    Mask phone number for logs (PII-safe).

    Args:
    phone: Raw phone number.
    keep_last: Number of last digits to keep unmasked.

    Returns:
    Masked phone string.
    """

    if not phone:
        return ""
    tail = phone[-keep_last:]
    return "*" * max(0, len(phone) - keep_last) + tail