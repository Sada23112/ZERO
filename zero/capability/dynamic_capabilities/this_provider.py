"""Dynamically synthesized provider for this."""

import httpx
from typing import List, Optional, Any, Dict, AsyncGenerator
from providers.base import BaseProvider
from models.model import DiscoveredModel
from models.conversation import Message, MessageRole
from zero_logging import logger

class ThisGeneratedProvider(BaseProvider):
    def __init__(self, api_key: str = "sk-deepmind-secret-key-12345", base_url: str = "https://api.deepmind-custom.ai/v1"):
        self._name = "this"
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    @property
    def name(self) -> str:
        return self._name

    async def generate_response(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        target_model = model or "this-default"
        prompt = messages[-1].content if messages else ""
        # Check endpoint
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": target_model, "messages": [{"role": "user", "content": prompt}]}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
        except Exception:
            pass
        return f"[THIS Provider] Synthesized response for: {prompt}"

    async def stream_generate(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        res = await self.generate_response(messages, model, system_instruction, **kwargs)
        for token in res.split():
            yield token + " "

    async def discover_models(self, force_refresh: bool = False) -> List[DiscoveredModel]:
        return [DiscoveredModel(id="this-default", display_name="This Default Model")]
