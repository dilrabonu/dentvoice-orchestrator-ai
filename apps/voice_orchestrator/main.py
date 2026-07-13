""" FastAPI entrypoint for the Voice Orchestrator AI Service."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from apps.voice_orchestrator.config import settings
from core.dialog_manager.state_machine import DialogSession
from observability.logging_config import get_logger