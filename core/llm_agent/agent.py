from __future__ import annotations

class LLMAgent:
    def __init__(self, system_prompt: str, tools: list[dict]) -> None:
        self.system_prompt = system_prompt
        self.tools = tools

    async def step(self, history: list[dict], user_text: str) -> tuple[str, list[dict]]:
        
