"""Project ZERO — Capability Marketplace.

Catalog for discovering, browsing, and installing built-in and external capabilities.
"""

from typing import List, Dict, Any, Optional, Tuple
from zero_logging import logger
from zero.capability.provider_factory import KNOWN_PROVIDER_ENDPOINTS


BUILTIN_MARKETPLACE_CATALOG = [
    # Providers
    {"name": "openai", "category": "provider", "version": "1.0.0", "description": "OpenAI GPT-4o & GPT-4o-mini provider", "author": "ZERO Core"},
    {"name": "claude", "category": "provider", "version": "1.0.0", "description": "Anthropic Claude 3.5 Sonnet & Haiku provider", "author": "ZERO Core"},
    {"name": "gemini", "category": "provider", "version": "1.0.0", "description": "Google Gemini 2.5 Flash & Pro provider", "author": "ZERO Core"},
    {"name": "grok", "category": "provider", "version": "1.0.0", "description": "xAI Grok provider", "author": "ZERO Core"},
    {"name": "ollama", "category": "provider", "version": "1.0.0", "description": "Ollama Local LLM Runner provider", "author": "ZERO Core"},
    {"name": "lmstudio", "category": "provider", "version": "1.0.0", "description": "LM Studio Local Endpoint provider", "author": "ZERO Core"},
    {"name": "openrouter", "category": "provider", "version": "1.0.0", "description": "OpenRouter Unified LLM Gateway", "author": "ZERO Core"},
    {"name": "nvidia", "category": "provider", "version": "1.0.0", "description": "NVIDIA NIM Inference Cloud provider", "author": "ZERO Core"},
    {"name": "together", "category": "provider", "version": "1.0.0", "description": "Together AI Open Source LLM Cloud provider", "author": "ZERO Core"},
    {"name": "deepseek", "category": "provider", "version": "1.0.0", "description": "DeepSeek V3 & R1 Reasoning provider", "author": "ZERO Core"},

    # Memory Backends
    {"name": "sqlite", "category": "memory", "version": "1.0.0", "description": "SQLite Relational & Memory Storage Backend", "author": "ZERO Core"},
    {"name": "postgresql", "category": "memory", "version": "1.0.0", "description": "PostgreSQL High Performance Enterprise Memory", "author": "ZERO Core"},
    {"name": "chromadb", "category": "memory", "version": "1.0.0", "description": "ChromaDB Vector Embeddings Backend", "author": "ZERO Core"},

    # Planners
    {"name": "long_running", "category": "planner", "version": "1.0.0", "description": "Long-Running Planning Engine with Task Deconstruction", "author": "ZERO Core"},
    {"name": "hierarchical", "category": "planner", "version": "1.0.0", "description": "Hierarchical Task Network (HTN) Planner", "author": "ZERO Core"},

    # Voice Engines
    {"name": "pyttsx3", "category": "voice", "version": "1.0.0", "description": "pyttsx3 Offline TTS Engine", "author": "ZERO Core"},
    {"name": "elevenlabs", "category": "voice", "version": "1.0.0", "description": "ElevenLabs Neural Voice Synthesis Engine", "author": "ZERO Community"},

    # OCR Engines
    {"name": "tesseract", "category": "ocr", "version": "1.0.0", "description": "Tesseract OCR Engine", "author": "ZERO Core"},
    {"name": "easyocr", "category": "ocr", "version": "1.0.0", "description": "EasyOCR PyTorch Visual Text Extractor", "author": "ZERO Community"},

    # Browser Engines
    {"name": "playwright", "category": "browser", "version": "1.0.0", "description": "Playwright Headless Web Automation", "author": "ZERO Core"},
    {"name": "selenium", "category": "browser", "version": "1.0.0", "description": "Selenium Web Driver Automation Engine", "author": "ZERO Community"},
]


class CapabilityMarketplace:
    """Marketplace for searching and discovering ZERO capabilities."""

    def __init__(self) -> None:
        self._catalog = list(BUILTIN_MARKETPLACE_CATALOG)

    def list_available(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List available capabilities in catalog."""
        if category:
            cat_lower = category.lower().strip()
            return [item for item in self._catalog if item.get("category", "").lower() == cat_lower]
        return list(self._catalog)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search catalog by keyword query."""
        q = query.lower().strip()
        results = []
        for item in self._catalog:
            if q in item["name"].lower() or q in item["description"].lower() or q in item["category"].lower():
                results.append(item)
        return results

    def get_item(self, name: str) -> Optional[Dict[str, Any]]:
        """Fetch item metadata by name."""
        n = name.lower().strip()
        for item in self._catalog:
            if item["name"].lower() == n:
                return item
        return None
