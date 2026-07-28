"""Project ZERO — OS Process Manager (Phase 7)."""

import psutil
from typing import List, Dict, Any, Optional


class OSProcessManager:
    """Manages system processes across operating system."""

    @staticmethod
    def list_running_processes(limit: int = 15) -> List[Dict[str, Any]]:
        """Return list of top running processes ordered by CPU usage."""
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                procs.append({
                    "pid": p.info['pid'],
                    "name": p.info['name'],
                    "cpu_percent": p.info['cpu_percent'],
                    "memory_mb": round(p.info['memory_info'].rss / (1024 * 1024), 1)
                })
            except Exception:
                pass

        procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return procs[:limit]

    @staticmethod
    def kill_process(pid_or_name: str) -> bool:
        """Terminate process by PID or name."""
        try:
            if pid_or_name.isdigit():
                p = psutil.Process(int(pid_or_name))
                p.terminate()
                return True
            else:
                for p in psutil.process_iter(['name']):
                    if p.info['name'] and pid_or_name.lower() in p.info['name'].lower():
                        p.terminate()
                        return True
        except Exception:
            pass
        return False
