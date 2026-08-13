"""Structured logging (JSON in prod, readable console in dev).

Every log call in the app uses key=value fields (call_id, tenant_id,
latency_ms, etc.) so logs are queryable once shipped to a log backend
(Phase 9/10 - Loki/ELK/Datadog, whichever the clinic's infra ends up using).
"""
from __future__ import annotations

import logging
import sys

import structurelog

def configure_logging(level: str = "INFO", json_output: bool = False) -> None:
    logging.basicConfig(
        format
    )
