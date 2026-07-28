"""Project ZERO — Gemini Provider & Dynamic Model Discovery."""

from typing import List, Optional, Any, Dict
import httpx
from google import genai
from providers.base import BaseProvider
from models.model import DiscoveredModel
from models.conversation import Message, MessageRole
from zero_logging import logger


class GeminiProvider(BaseProvider):
    """Google Gemini API Provider featuring mandatory dynamic model discovery."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._cached_models: List[DiscoveredModel] = []
        self._client: Optional[genai.Client] = None
        if api_key and api_key.strip():
            try:
                self._client = genai.Client(api_key=api_key.strip())
            except Exception as e:
                logger.warning(f"Failed to initialize google-genai Client: {e}")

    @property
    def name(self) -> str:
        return "gemini"

    async def discover_models(self, force_refresh: bool = False) -> List[DiscoveredModel]:
        """Dynamically query Google Generative Language API for models supporting generateContent."""
        if not self.api_key or not self.api_key.strip():
            logger.warning("Gemini API key is empty. Cannot discover models.")
            return []

        if not force_refresh and self._cached_models:
            return self._cached_models

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key.strip()}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    models_json = data.get("models", [])
                    discovered: List[DiscoveredModel] = []
                    for m in models_json:
                        methods = m.get("supportedGenerationMethods", [])
                        if "generateContent" in methods:
                            model_id = m.get("name", "").replace("models/", "")
                            discovered.append(
                                DiscoveredModel(
                                    id=model_id,
                                    display_name=m.get("displayName", model_id),
                                    version=m.get("version", "latest"),
                                    description=m.get("description"),
                                    input_token_limit=m.get("inputTokenLimit"),
                                    output_token_limit=m.get("outputTokenLimit"),
                                    supported_methods=methods
                                )
                            )
                    self._cached_models = discovered
                    logger.info(f"Discovered {len(discovered)} Gemini models dynamically.")
                    return discovered
                else:
                    logger.error(f"Gemini Model Discovery API returned HTTP {resp.status_code}")
        except Exception as err:
            logger.error(f"Failed dynamic Gemini model discovery: {err}")

        return self._cached_models

    async def generate_response(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate content from Gemini model API."""
        if not self.api_key or not self.api_key.strip():
            return "[Error: Gemini API key is missing. Run `config` command to set key.]"

        target_model = model or "gemini-2.0-flash"

        # Format conversation messages for Gemini API
        contents: List[Dict[str, Any]] = []
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                system_instruction = msg.content
                continue

            role_str = "user" if msg.role == MessageRole.USER else "model"
            contents.append({"role": role_str, "parts": [{"text": msg.content}]})

        if not contents:
            return "[Error: No user messages provided for generation.]"

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={self.api_key.strip()}"
            payload: Dict[str, Any] = {"contents": contents}

            if system_instruction:
                payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"]
                    return "[Empty response from Gemini API]"
                else:
                    return f"[Error: Gemini API HTTP {resp.status_code}: {resp.text}]"
        except Exception as err:
            logger.error(f"Gemini generateContent error: {err}")
            return f"[Error during generation: {str(err)}]"
