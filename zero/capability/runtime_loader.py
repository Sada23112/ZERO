"""Project ZERO — Dynamic Runtime Code Loader.

Loads modules, classes, and python code dynamically at runtime using importlib.
"""

import sys
import os
import types
import importlib
import importlib.util
from pathlib import Path
from typing import Any, Optional, Type
from zero_logging import logger


class RuntimeLoader:
    """Dynamic code loader for runtime capabilities."""

    @staticmethod
    def load_module_from_file(file_path: str, module_name: Optional[str] = None) -> types.ModuleType:
        """Dynamically load a python module from a file path."""
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        name = module_name or path.stem
        spec = importlib.util.spec_from_file_location(name, str(path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec for module at {file_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        logger.info(f"[RuntimeLoader] Successfully loaded module '{name}' from {path}")
        return module

    @staticmethod
    def load_module_from_code(code: str, module_name: str) -> types.ModuleType:
        """Dynamically compile and execute python code as an in-memory module."""
        module = types.ModuleType(module_name)
        module.__file__ = f"<dynamic_module:{module_name}>"
        sys.modules[module_name] = module
        exec(code, module.__dict__)
        logger.info(f"[RuntimeLoader] Compiled and loaded in-memory module '{module_name}'")
        return module

    @staticmethod
    def load_class_from_module(module: types.ModuleType, class_name: str) -> Type[Any]:
        """Extract target class from loaded module."""
        if not hasattr(module, class_name):
            raise AttributeError(f"Module '{module.__name__}' has no attribute/class '{class_name}'")
        cls = getattr(module, class_name)
        if not isinstance(cls, type):
            raise TypeError(f"Attribute '{class_name}' in module '{module.__name__}' is not a class/type")
        return cls

    @classmethod
    def load_class(cls, entry_point: str) -> Type[Any]:
        """Load class using entry point syntax 'module.path:ClassName' or 'module.path.ClassName'."""
        if ":" in entry_point:
            module_str, class_name = entry_point.split(":", 1)
        elif "." in entry_point:
            parts = entry_point.rsplit(".", 1)
            module_str, class_name = parts[0], parts[1]
        else:
            raise ValueError(f"Invalid entry point syntax: '{entry_point}'. Expected 'module:ClassName' or 'module.ClassName'")

        if os.path.exists(module_str):
            module = cls.load_module_from_file(module_str)
        else:
            module = importlib.import_module(module_str)

        return cls.load_class_from_module(module, class_name)

    @staticmethod
    def unload_module(module_name: str) -> None:
        """Safely remove module from sys.modules."""
        if module_name in sys.modules:
            del sys.modules[module_name]
            logger.info(f"[RuntimeLoader] Unloaded module '{module_name}' from sys.modules")
