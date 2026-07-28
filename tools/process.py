"""Project ZERO — Process Manager & System Hardware Monitor (Phase 4 Capability #10)."""

import os
from typing import Dict, Any, Optional, List
from tools.base import BaseTool
from models.tool import ToolDefinition, ToolResult, ToolParameter
from zero_logging import logger

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class ProcessManagerTool(BaseTool):
    """Tool to inspect active OS processes and hardware metrics (CPU, RAM, Disk, Battery)."""

    @property
    def name(self) -> str:
        return "process_manager"

    @property
    def description(self) -> str:
        return "List active processes, kill processes by PID/Name, and inspect CPU/RAM/Disk/Battery system metrics."

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "action": ToolParameter(type="string", description="Action: 'list', 'metrics', 'kill'"),
                "target": ToolParameter(type="string", description="Target PID or process name for kill action", required=False)
            }
        )

    async def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        action = arguments.get("action", "metrics").strip().lower()
        target = arguments.get("target", "").strip()

        if not PSUTIL_AVAILABLE:
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="psutil library is not installed.")

        try:
            if action == "metrics":
                cpu_pct = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage("/")
                battery = getattr(psutil, "sensors_battery", lambda: None)()

                battery_str = f"{battery.percent}% ({'Charging' if battery.power_plugged else 'Discharging'})" if battery else "N/A"

                out = (
                    f"System Hardware Metrics:\n"
                    f"- CPU Usage: {cpu_pct}%\n"
                    f"- RAM Usage: {mem.percent}% ({mem.used // (1024*1024)} MB / {mem.total // (1024*1024)} MB)\n"
                    f"- Disk Usage: {disk.percent}% ({disk.used // (1024*1024*1024)} GB / {disk.total // (1024*1024*1024)} GB)\n"
                    f"- Battery Level: {battery_str}\n"
                )
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=out)

            elif action == "list":
                procs = []
                for p in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
                    try:
                        procs.append(f"PID {p.info['pid']:<6} | {p.info['name']:<25} | Mem: {p.info['memory_percent']:.1f}%")
                    except Exception:
                        pass
                return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Active System Processes ({len(procs)}):\n" + "\n".join(procs[:25]))

            elif action == "kill":
                if not target:
                    return ToolResult(call_id=call_id, tool_name=self.name, success=False, error="Argument 'target' (PID or name) required to kill process.")

                if target.isdigit():
                    pid = int(target)
                    p = psutil.Process(pid)
                    p.terminate()
                    return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Terminated process PID {pid}")
                else:
                    count = 0
                    for p in psutil.process_iter(["pid", "name"]):
                        if target.lower() in p.info["name"].lower():
                            p.terminate()
                            count += 1
                    return ToolResult(call_id=call_id, tool_name=self.name, success=True, output=f"Terminated {count} process(es) matching '{target}'.")

            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=f"Unknown process manager action '{action}'.")

        except Exception as err:
            logger.error(f"Process manager action failed: {err}")
            return ToolResult(call_id=call_id, tool_name=self.name, success=False, error=str(err))
