"""Project ZERO — Gemini Provider & Dynamic Model Discovery."""

import re
import json
import asyncio
from typing import List, Optional, Any, Dict, AsyncGenerator
import httpx
from google import genai
from providers.base import BaseProvider
from models.model import DiscoveredModel
from models.conversation import Message, MessageRole
from zero_logging import logger

FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]


class GeminiProvider(BaseProvider):
    """Google Gemini API Provider featuring mandatory dynamic model discovery & rate limit failover."""

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

                    # Sort models so stable & latest versions (3.6, 3.5, 2.5, 2.0) appear first
                    discovered.sort(key=self._model_sort_key, reverse=True)

                    self._cached_models = discovered
                    logger.info(f"Discovered {len(discovered)} Gemini models dynamically.")
                    return discovered
                else:
                    logger.error(f"Gemini Model Discovery API returned HTTP {resp.status_code}")
        except Exception as err:
            logger.error(f"Failed dynamic Gemini model discovery: {err}")

        return self._cached_models

    def _model_sort_key(self, model: DiscoveredModel) -> float:
        """Helper to rank latest Gemini models higher in display tables."""
        model_id = model.id.lower()
        match = re.search(r"gemini-(\d+\.\d+|\d+)", model_id)
        if match:
            try:
                version_score = float(match.group(1)) * 100.0
            except ValueError:
                version_score = 10.0
        elif "latest" in model_id:
            version_score = 90.0
        else:
            version_score = 1.0

        if "flash" in model_id:
            version_score += 5.0
        elif "pro" in model_id:
            version_score += 4.0

        if "tts" in model_id or "image" in model_id:
            version_score -= 50.0

        return version_score

    async def generate_response(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate content from Gemini model API with rate-limit failover."""
        if not self.api_key or not self.api_key.strip():
            return "[Error: Gemini API key is missing. Update GEMINI_API_KEY in .env.]"

        primary_model = model or "gemini-2.5-flash"
        models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]

        contents: List[Dict[str, Any]] = []
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                system_instruction = msg.content
                continue
            role_str = "user" if msg.role == MessageRole.USER else "model"
            contents.append({"role": role_str, "parts": [{"text": msg.content}]})

        if not contents:
            return "[Error: No user messages provided for generation.]"

        for target_model in models_to_try:
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

                    elif resp.status_code == 429:
                        logger.warning(f"Rate limit HTTP 429 on model '{target_model}'. Trying next fallback model...")
                        await asyncio.sleep(0.5)
                        continue
                    else:
                        logger.error(f"Gemini API returned HTTP {resp.status_code}: {resp.text}")
                        return f"[Error: Gemini API HTTP {resp.status_code}: {resp.text}]"

            except Exception as err:
                logger.error(f"Gemini generateContent error for {target_model}: {err}")

        return "[Error: Rate limit (HTTP 429) quota exceeded across all available Gemini models. Please wait a moment or check your API quota at https://aistudio.google.com/.]"

    async def stream_generate(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """Stream response text chunks from Gemini API with fallback to non-streaming when rate limited."""
        if not self.api_key or not self.api_key.strip():
            yield "[Error: Gemini API key is missing. Set GEMINI_API_KEY in .env.]"
            return

        target_model = model or "gemini-2.5-flash"

        contents: List[Dict[str, Any]] = []
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                system_instruction = msg.content
                continue
            role_str = "user" if msg.role == MessageRole.USER else "model"
            contents.append({"role": role_str, "parts": [{"text": msg.content}]})

        if not contents:
            yield "[Error: No contents provided]"
            return

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:streamGenerateContent?key={self.api_key.strip()}&alt=sse"
        payload: Dict[str, Any] = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        stream_failed_429 = False

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, json=payload) as response:
                    if response.status_code == 429:
                        stream_failed_429 = True
                    elif response.status_code != 200:
                        yield f"[Error streaming from Gemini: HTTP {response.status_code}]"
                        return
                    else:
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                json_str = line[6:].strip()
                                if json_str == "[DONE]":
                                    break
                                try:
                                    data = json.loads(json_str)
                                    candidates = data.get("candidates", [])
                                    if candidates and "content" in candidates[0]:
                                        parts = candidates[0]["content"].get("parts", [])
                                        if parts and "text" in parts[0]:
                                            yield parts[0]["text"]
                                except Exception:
                                    pass
                        return

        except Exception as err:
            logger.warning(f"Streaming failed: {err}. Attempting fallback response generation.")
            stream_failed_429 = True

        # Fallback if streaming endpoint returns 429 or fails
        if stream_failed_429:
            logger.info("Streaming hit rate limit (HTTP 429). Falling back to robust model generate_response...")
            fallback_text = await self.generate_response(messages, model=model, system_instruction=system_instruction)
            yield fallback_text
