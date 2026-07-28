"""Project ZERO — Storage Intelligence Manager (Phase 7)."""

import os
import psutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StorageReport(BaseModel):
    """Structured report of storage metrics and largest items."""

    total_gb: float
    used_gb: float
    free_gb: float
    percent_used: float
    largest_files: List[Dict[str, Any]] = Field(default_factory=list)


class StorageManager:
    """Provides disk space analytics, largest file finder, and storage intelligence."""

    def get_storage_report(self, target_dir: Optional[Path] = None) -> StorageReport:
        """Calculate disk space and locate largest files."""
        disk = psutil.disk_usage("/")
        scan_dir = target_dir or Path.home()

        largest: List[Dict[str, Any]] = []
        try:
            for root, dirs, files in os.walk(scan_dir):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["venv", "node_modules", "AppData", "Windows"]]

                for f in files:
                    fp = Path(root, f)
                    try:
                        sz = fp.stat().st_size
                        if sz > 10 * 1024 * 1024:  # > 10MB
                            largest.append({
                                "name": f,
                                "path": str(fp),
                                "size_mb": round(sz / (1024 * 1024), 2)
                            })
                    except Exception:
                        pass

            largest.sort(key=lambda x: x["size_mb"], reverse=True)
        except Exception:
            pass

        return StorageReport(
            total_gb=round(disk.total / (1024**3), 2),
            used_gb=round(disk.used / (1024**3), 2),
            free_gb=round(disk.free / (1024**3), 2),
            percent_used=disk.percent,
            largest_files=largest[:10]
        )
