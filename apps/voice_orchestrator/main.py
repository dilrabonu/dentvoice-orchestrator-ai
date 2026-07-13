""" FastAPI entrypoint for the Voice Orchestrator AI Service."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from apps.voice_orchestrator.config import settings
from core.dialog_manager.state_machine import DialogSession
from observability.logging_config import get_logger

logger = get_logger(__name__)

app = FastAPI(title="DentVoice Orchestrator AI", version="0.1.0")

@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "env": settings.app_env,
        "tenant": settings.tenant_id,
        "phase": "1-foundation",
    }

@app.websocket("/ws/call")
async def call_stream(websocket: WebSocket) -> None:
    """Placeholder for Twilio Media Streams audio WS 
    For now this only demonstrates that a call session can be created and
    driven by text messages, so the dialog manager can be smoke-tested over
    a WebSocket before real audio/STT/TTS are wired in.
    """
    await websocket.accept()