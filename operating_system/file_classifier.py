"""Project ZERO — File Classifier & Category Manager (Phase 7)."""

from pathlib import Path
from typing import Dict, List, Optional


class FileClassifier:
    """Classifies files by extension into core categories (documents, code, images, audio, video, archives)."""

    CATEGORIES = {
        "documents": [".pdf", ".docx", ".doc", ".txt", ".md", ".rtf", ".epub", ".odt"],
        "spreadsheets": [".xlsx", ".xls", ".csv", ".ods"],
        "presentations": [".pptx", ".ppt", ".key", ".odp"],
        "images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp"],
        "audio": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"],
        "video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"],
        "archives": [".zip", ".tar", ".gz", ".7z", ".rar", ".bz2"],
        "code": [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".dart", ".json", ".yaml", ".toml"]
    }

    @classmethod
    def classify(cls, path: str) -> str:
        """Return category name for a given file path or extension."""
        ext = Path(path).suffix.lower()
        for category, extensions in cls.CATEGORIES.items():
            if ext in extensions:
                return category
        return "other"

    @classmethod
    def get_extensions_for_category(cls, category: str) -> List[str]:
        """Return list of extensions for a category name."""
        return cls.CATEGORIES.get(category.lower(), [])
