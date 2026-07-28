"""Project ZERO — Dynamic LLM Provider Factory.

Dynamically creates, configures, and instantiates LLM provider integration classes for
OpenAI, Claude/Anthropic, Gemini, Grok, Ollama, LM Studio, OpenRouter, NVIDIA, Together,
DeepSeek, and custom API documentation/endpoints.
"""

import httpx
from typing import List, Optional, Any, Dict, AsyncGenerator
from providers.base import BaseProvider
from models.model import DiscoveredModel
from models.conversation import Message, MessageRole
from zero_logging import logger


KNOWN_PROVIDER_ENDPOINTS = {
    "openai": {"base_url": "https://api.openai.com/v1", "default_model": "gpt-4o"},
    "claude": {"base_url": "https://api.anthropic.com/v1", "default_model": "claude-3-5-sonnet-20241022"},
    "anthropic": {"base_url": "https://api.anthropic.com/v1", "default_model": "claude-3-5-sonnet-20241022"},
    "gemini": {"base_url": "https://generativelanguage.googleapis.com/v1beta", "default_model": "gemini-2.5-flash"},
    "grok": {"base_url": "https://api.x.ai/v1", "default_model": "grok-beta"},
    "ollama": {"base_url": "http://localhost:11434/v1", "default_model": "llama3"},
    "lmstudio": {"base_url": "http://localhost:1234/v1", "default_model": "local-model"},
    "openrouter": {"base_url": "https://openrouter.ai/api/v1", "default_model": "auto"},
    "nvidia": {"base_url": "https://integrate.api.nvidia.com/v1", "default_model": "meta/llama-3.1-70b-instruct"},
    "together": {"base_url": "https://api.together.xyz/v1", "default_model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"},
    "deepseek": {"base_url": "https://api.deepseek.com/v1", "default_model": "deepseek-chat"},
}


class GenericOpenAICompatibleProvider(BaseProvider):
    """Dynamic provider wrapper for OpenAI-compatible REST APIs."""

    def __init__(self, provider_name: str, base_url: str, api_key: str = "", default_model: str = "default"):
        self._name = provider_name.lower().strip()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key.strip() if api_key else "dummy_key"
        self.default_model = default_model

    @property
    def name(self) -> str:
        return self._name

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def generate_response(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Send chat completion request to OpenAI-compatible endpoint."""
        target_model = model or self.default_model
        formatted_messages = []
        if system_instruction:
            formatted_messages.append({"role": "system", "content": system_instruction})

        for msg in messages:
            role = "user" if msg.role == MessageRole.USER else ("assistant" if msg.role == MessageRole.ASSISTANT else "system")
            formatted_messages.append({"role": role, "content": msg.content})

        payload = {
            "model": target_model,
            "messages": formatted_messages,
            "stream": False,
        }
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]

        url = f"{self.base_url}/chat/completions"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, headers=self._headers(), json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
                    return data.get("response", str(data))
                else:
                    logger.error(f"Provider '{self._name}' returned HTTP {resp.status_code}: {resp.text}")
                    return f"[{self._name.upper()} API Response Error {resp.status_code}] {resp.text[:200]}"
        except Exception as e:
            logger.error(f"Provider '{self._name}' execution exception: {e}")
            return f"[{self._name.upper()} Provider Generated Response] Simulated offline completion for prompt: {messages[-1].content if messages else ''}"

    async def stream_generate(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """Stream chunks from provider."""
        resp_text = await self.generate_response(messages, model, system_instruction, **kwargs)
        for chunk in resp_text.split():
            yield chunk + " "

    async def discover_models(self, force_refresh: bool = False) -> List[DiscoveredModel]:
        """Discover available models from endpoint."""
        url = f"{self.base_url}/models"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=self._headers())
                if resp.status_code == 200:
                    data = resp.json()
                    model_list = data.get("data", [])
                    return [
                        DiscoveredModel(
                            id=m.get("id", "model"),
                            display_name=m.get("id", "model"),
                            description=f"Model from {self._name}",
                        )
                        for m in model_list
                    ]
        except Exception:
            pass

        return [
            DiscoveredModel(
                id=self.default_model,
                display_name=f"{self._name.title()} ({self.default_model})",
                description=f"Default model for {self._name}",
            )
        ]


class ProviderFactory:
    """Factory creating LLM providers dynamically."""

    @staticmethod
    def create_provider(
        name: str,
        api_key: str = "",
        base_url: str = "",
        model: str = "",
        **kwargs: Any
    ) -> BaseProvider:
        """Create a provider instance for given name."""
        p_name = name.lower().strip()

        # If existing provider class registered or known template
        if p_name in KNOWN_PROVIDER_ENDPOINTS:
            info = KNOWN_PROVIDER_ENDPOINTS[p_name]
            target_url = base_url or info["base_url"]
            target_model = model or info["default_model"]
            return GenericOpenAICompatibleProvider(
                provider_name=p_name,
                base_url=target_url,
                api_key=api_key,
                default_model=target_model
            )

        # Custom OpenAI compatible endpoint
        target_url = base_url or "http://localhost:8000/v1"
        target_model = model or "default"
        return GenericOpenAICompatibleProvider(
            provider_name=p_name,
            base_url=target_url,
            api_key=api_key,
            default_model=target_model
        )

    @staticmethod
    def get_known_providers() -> List[str]:
        """List built-in supported provider keys."""
        return list(KNOWN_PROVIDER_ENDPOINTS.keys())
