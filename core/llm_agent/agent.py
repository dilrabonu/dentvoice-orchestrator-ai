from __future__ import annotations

class LLMAgent:
    def __init__(self, system_prompt: str, tools: list[dict]) -> None:
        self.system_prompt = system_prompt
        self.tools = tools
        
