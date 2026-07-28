#!/usr/bin/env python3
"""Project ZERO — Personal Autonomous Intelligence Platform.

Entrypoint for interactive terminal shell and CLI execution.
"""

import sys
import asyncio
from cli.shell import ZeroShell


def main() -> None:
    """Launch Project ZERO interactive shell."""
    try:
        shell = ZeroShell()
        asyncio.run(shell.run())
    except KeyboardInterrupt:
        print("\nSession ended.")
        sys.exit(0)


if __name__ == "__main__":
    main()
