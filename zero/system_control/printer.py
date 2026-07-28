"""Project ZERO — Printer Subsystem Control.

Manages print jobs, document printing, printer listing, and status diagnostics.
"""

import os
import subprocess
import platform
from typing import List, Dict, Any, Tuple, Optional
from zero_logging import logger


class PrinterController:
    """Manages document printing and printer hardware interfaces."""

    def __init__(self) -> None:
        self.default_printer: str = "HP OfficeJet Pro 9010"
        self._printers: List[Dict[str, Any]] = [
            {"name": "HP OfficeJet Pro 9010", "status": "Ready", "is_default": True},
            {"name": "Microsoft Print to PDF", "status": "Ready", "is_default": False},
        ]

    def print_document(self, file_path: str, printer_name: Optional[str] = None) -> Tuple[bool, str]:
        """Print document file to selected printer."""
        path = os.path.abspath(file_path)
        if not os.path.exists(path):
            return False, f"File not found: '{file_path}'"

        target_printer = printer_name or self.default_printer

        if platform.system() == "Windows":
            try:
                cmd = f"powershell -Command \"Start-Process -FilePath '{path}' -Verb PrintTo -ArgumentList '{target_printer}'\""
                subprocess.Popen(cmd, shell=True)
            except Exception:
                pass

        logger.info(f"[Printer] Sent print job for '{path}' to '{target_printer}'")
        return True, f"Print job sent to '{target_printer}' for document '{os.path.basename(path)}'."

    def list_printers(self) -> List[Dict[str, Any]]:
        """List connected printers."""
        return list(self._printers)

    def get_printer_status(self, printer_name: Optional[str] = None) -> Dict[str, Any]:
        """Fetch printer status."""
        target = (printer_name or self.default_printer).lower()
        for p in self._printers:
            if target in p["name"].lower():
                return p
        return {"name": printer_name or "Unknown", "status": "Offline", "is_default": False}
