from __future__ import annotations

import uuid
from datetime import datetime, timedelta

from observability.logging_config import get_logger
from tools.schemas import Booking, Customer

logger = get_logger(__name__)
