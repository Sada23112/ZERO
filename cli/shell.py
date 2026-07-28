"""Project ZERO — Interactive Terminal REPL Subsystem."""

import sys
import asyncio
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from brain.brain import Brain
from zero_logging import logger

console = Console()


class ZeroShell:
    """Thin interactive CLI shell delegating input processing to Brain."""

    def __init__(self, brain: Optional[Brain] = None):
        self.brain = brain or Brain()

    def print_welcome(self):
        """Display ZERO v0.1 welcome header banner."""
        banner = (
            "[bold blue]ZERO v0.1[/bold blue] — Personal Autonomous Intelligence Platform\n"
            "[dim]Python-First Core Infrastructure • Type 'help' for commands • 'exit' to quit[/dim]"
        )
        console.print(Panel(banner, border_style="blue", title="[bold white]Project ZERO[/bold white]"))

    def print_help(self):
        """Display help command table."""
        table = Table(title="Project ZERO Commands", border_style="dim")
        table.add_column("Command / Intent", style="bold cyan", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("help", "Display available shell commands")
        table.add_row("models", "Dynamically discover & list available provider models")
        table.add_row("config", "Inspect current system configuration settings")
        table.add_row("remember that <x> uses <y>", "Store project or preference memory record")
        table.add_row("what framework does <x> use?", "Query cognitive memory for framework or fact")
        table.add_row("list memories", "List stored cognitive key-value memory records")
        table.add_row("search memory <query>", "Keyword search stored memory records")
        table.add_row("read <filepath>", "Read and display contents of a local file")
        table.add_row("summarize <folder>", "Summarize directory file listing")
        table.add_row("run <command>", "Execute shell command safely via process subexec")
        table.add_row("open <url>", "Fetch and extract text content from web URL")
        table.add_row("history", "View session transcript history")
        table.add_row("clear", "Clear terminal console buffer")
        table.add_row("exit / quit", "Terminate ZERO terminal session")

        console.print(table)

    async def cmd_models(self):
        """Execute dynamic Gemini model discovery and render model catalog."""
        console.print("[dim]Fetching available models dynamically from provider API...[/dim]")
        models = await self.brain.provider.discover_models(force_refresh=True)

        if not models:
            console.print("[bold yellow]No models returned. Verify GEMINI_API_KEY in .env.[/bold yellow]")
            return

        table = Table(title=f"Discovered Gemini Models ({len(models)})", border_style="blue")
        table.add_column("Model ID", style="bold cyan")
        table.add_column("Display Name", style="bold white")
        table.add_column("Input Tokens", style="dim")
        table.add_column("Output Tokens", style="dim")

        for m in models:
            table.add_row(
                m.id,
                m.display_name,
                str(m.input_token_limit or "-"),
                str(m.output_token_limit or "-")
            )

        console.print(table)

    def cmd_config(self):
        """Inspect system configuration settings."""
        table = Table(title="System Settings (.env & zero-settings.json)", border_style="magenta")
        table.add_column("Configuration Key", style="bold cyan")
        table.add_column("Current Value", style="bold white")

        s = self.brain.settings
        table.add_row("GEMINI_API_KEY", "***configured***" if s.gemini_api_key else "[red]Not Configured[/red]")
        table.add_row("DEFAULT_PROVIDER", s.default_provider)
        table.add_row("DEFAULT_MODEL", s.default_model)
        table.add_row("DATABASE_PATH", s.database_path)
        table.add_row("LOG_LEVEL", s.log_level)
        table.add_row("DEBUG", str(s.debug))

        console.print(table)

    def cmd_history(self):
        """Inspect transcript history for active session."""
        messages = self.brain.conversation_manager.load_history()
        if not messages:
            console.print("[dim]No messages in current session history.[/dim]")
            return

        table = Table(title=f"Session Transcript History ({len(messages)} messages)", border_style="green")
        table.add_column("Role", style="bold cyan")
        table.add_column("Content", style="white")
        table.add_column("Timestamp", style="dim")

        for msg in messages:
            table.add_row(msg.role.value, msg.content, msg.created_at[:19])

        console.print(table)

    async def handle_prompt(self, user_input: str):
        """Delegate input processing to Brain and display response."""
        console.print("\n[bold blue]ZERO:[/bold blue] ", end="")
        
        # Stream response chunks live
        full_text = []
        async for chunk in self.brain.process_stream(user_input):
            console.print(chunk, end="")
            full_text.append(chunk)

        console.print("\n")

    async def run(self):
        """Main thin CLI REPL command loop."""
        self.print_welcome()

        while True:
            try:
                user_input = Prompt.ask("[bold cyan]ZERO[/bold cyan] >").strip()
                if not user_input:
                    continue

                cmd_lower = user_input.lower()

                if cmd_lower in ["exit", "quit"]:
                    console.print("[dim]Exiting Project ZERO...[/dim]")
                    break
                elif cmd_lower == "help":
                    self.print_help()
                elif cmd_lower == "clear":
                    console.clear()
                    self.print_welcome()
                elif cmd_lower == "models":
                    await self.cmd_models()
                elif cmd_lower == "config":
                    self.cmd_config()
                elif cmd_lower == "history":
                    self.cmd_history()
                else:
                    await self.handle_prompt(user_input)

            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Session terminated.[/dim]")
                break
            except Exception as err:
                console.print(f"[bold red]Error:[/bold red] {err}")
