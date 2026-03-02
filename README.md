# DentVoice Orchestrator AI

Production-grade real-time Voice AI Agent with:

- Streaming STT
- Tool orchestration
- Idempotent booking system
- Barge-in support
- Telephony integration (Twilio / SIP)
- Observability layer

## Architecture

Caller → Telephony → Streaming Audio → STT → Dialog Manager → Tools → TTS → Caller

## Tech Stack

- FastAPI
- Python 3.11+
- Streaming STT (Whisper / Deepgram / OpenAI)
- Structured Logging
- Docker-ready

## Project Structure
