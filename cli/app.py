"""Project ZERO — Typer CLI Entrypoint Application."""

import asyncio
import typer
from rich.console import Console
from cli.shell import ZeroShell

app = typer.Typer(
    name="zero",
    help="Project ZERO — Personal Autonomous Intelligence Platform CLI",
    add_completion=False
)
console = Console()


@app.command()
def shell():
    """Launch the interactive Project ZERO terminal shell REPL."""
    zero_shell = ZeroShell()
    asyncio.run(zero_shell.run())


@app.command()
def models():
    """Discover available LLM models dynamically from provider API."""
    zero_shell = ZeroShell()
    asyncio.run(zero_shell.cmd_models())


@app.command()
def config():
    """Display current runtime settings and environment variables."""
    zero_shell = ZeroShell()
    zero_shell.cmd_config()


if __name__ == "__main__":
    app()
