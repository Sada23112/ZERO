"""Project ZERO — Environment Awareness (Phase 6)."""

import os
import sys
import platform
import psutil
from typing import Dict, Any, Optional


class EnvironmentAwareness:
    """Tracks OS, Python, hardware metrics, current directory, & virtualenv."""

    def __init__(self):
        self._cached_env: Optional[Dict[str, Any]] = None
        self._last_refresh: float = 0.0

    def get_environment_info(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Fetch system environment info with caching to avoid overhead."""
        import time
        now = time.time()
        if not force_refresh and self._cached_env and (now - self._last_refresh < 30):
            return self._cached_env

        cpu_perc = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        battery = psutil.sensors_battery()

        self._cached_env = {
            "os": f"{platform.system()} {platform.release()}",
            "python_version": sys.version.split()[0],
            "current_dir": os.getcwd(),
            "virtual_env": os.environ.get("VIRTUAL_ENV", "None"),
            "cpu_usage": f"{cpu_perc}%",
            "ram_usage": f"{mem.percent}% ({mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB)",
            "disk_usage": f"{disk.percent}% ({disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB)",
            "battery": f"{battery.percent}% ({'Charging' if battery.power_plugged else 'Discharging'})" if battery else "N/A"
        }
        self._last_refresh = now
        return self._cached_env
