"""Project ZERO — Interactive Terminal REPL Subsystem."""

import sys
import asyncio
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from config import get_settings
from memory import DatabaseManager, ConversationRepository, MemoryRepository
from memory.repository import MemoryCategory
from providers import GeminiProvider, provider_registry
from models.conversation import Message, MessageRole

console = Console()


class ZeroShell:
    """Interactive REPL terminal shell for Project ZERO."""

    def __init__(self):
        self.settings = get_settings()
        self.db_manager = DatabaseManager(self.settings.database_path)
        self.conv_repo = ConversationRepository(self.db_manager)
        self.mem_repo = MemoryRepository(self.db_manager)

        # Initialize default session & providers
        self.active_session = self.conv_repo.create_session("Interactive Shell Session")
        self.gemini_provider = GeminiProvider(self.settings.gemini_api_key)
        provider_registry.register_provider(self.gemini_provider)

    def print_welcome(self):
        """Display ZERO v0.1 welcome header banner."""
        banner = (
            "[bold blue]ZERO v0.1[/bold blue] — Personal Autonomous Intelligence Platform\n"
            "[dim]Python-First Core Infrastructure • Type 'help' for commands • 'exit' to quit[/dim]"
        )
        console.print(Panel(banner, border_style="blue", title="[bold white]Project ZERO[/bold white]"))

    def print_help(self):
        """Display help command table."""
        table = Table(title="Project ZERO REPL Commands", border_style="dim")
        table.add_column("Command", style="bold cyan", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("help", "Display available shell commands")
        table.add_row("models", "Dynamically discover & list available provider models")
        table.add_row("config", "Inspect current system configuration settings")
        table.add_row("memory [set <k> <v>]", "View or store cognitive key-value memory records")
        table.add_row("history", "View message transcript history for active session")
        table.add_row("clear", "Clear terminal console output buffer")
        table.add_row("exit / quit", "Terminate ZERO terminal session")

        console.print(table)

    async def cmd_models(self):
        """Execute dynamic Gemini model discovery and render model catalog."""
        console.print("[dim]Fetching available models dynamically from provider API...[/dim]")
        models = await self.gemini_provider.discover_models(force_refresh=True)

        if not models:
            console.print("[bold yellow]No models returned. Verify GEMINI_API_KEY using `config` command.[/bold yellow]")
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
        """Inspect and manage system configuration settings."""
        table = Table(title="System Settings (.env & zero-settings.json)", border_style="magenta")
        table.add_column("Configuration Key", style="bold cyan")
        table.add_column("Current Value", style="bold white")

        table.add_row("GEMINI_API_KEY", "***configured***" if self.settings.gemini_api_key else "[red]Not Configured[/red]")
        table.add_row("DEFAULT_PROVIDER", self.settings.default_provider)
        table.add_row("DEFAULT_MODEL", self.settings.default_model)
        table.add_row("DATABASE_PATH", self.settings.database_path)
        table.add_row("LOG_LEVEL", self.settings.log_level)
        table.add_row("DEBUG", str(self.settings.debug))

        console.print(table)

    def cmd_memory(self, args: str):
        """View or store key-value memory records."""
        parts = args.strip().split()
        if len(parts) >= 3 and parts[0] == "set":
            key = parts[1]
            val = " ".join(parts[2:])
            record = self.mem_repo.set_memory(key=key, value=val, category=MemoryCategory.USER_PREFERENCE)
            console.print(f"[bold green]Saved memory record:[/bold green] {record.key} -> {record.value}")
            return

        memories = self.mem_repo.list_memories()
        if not memories:
            console.print("[dim]No cognitive memory records saved yet. Use `memory set <key> <val>`.[/dim]")
            return

        table = Table(title=f"Cognitive Memory Records ({len(memories)})", border_style="purple")
        table.add_column("Key", style="bold cyan")
        table.add_column("Value", style="white")
        table.add_column("Category", style="dim")
        table.add_column("Updated At", style="dim")

        for mem in memories:
            table.add_row(mem.key, mem.value, mem.category.value, mem.updated_at[:19])

        console.print(table)

    def cmd_history(self):
        """Inspect transcript history for current session."""
        messages = self.conv_repo.get_session_messages(self.active_session.id)
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
        """Process user natural language prompt and generate response."""
        user_msg = Message(
            session_id=self.active_session.id,
            role=MessageRole.USER,
            content=user_input
        )
        self.conv_repo.add_message(user_msg)

        console.print("[dim]Generating response...[/dim]")
        
        # Load history for context
        history = self.conv_repo.get_session_messages(self.active_session.id)
        
        response_text = await self.gemini_provider.generate_response(
            messages=history,
            model=self.settings.default_model
        )

        assistant_msg = Message(
            session_id=self.active_session.id,
            role=MessageRole.ASSISTANT,
            content=response_text,
            model=self.settings.default_model
        )
        self.conv_repo.add_message(assistant_msg)

        console.print(f"\n[bold blue]ZERO:[/bold blue] {response_text}\n")

    async def run(self):
        """Main REPL command loop."""
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
                elif cmd_lower.startswith("memory"):
                    self.cmd_memory(user_input[6:].strip())
                elif cmd_lower == "history":
                    self.cmd_history()
                else:
                    await self.handle_prompt(user_input)

            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Session terminated.[/dim]")
                break
            except Exception as err:
                console.print(f"[bold red]Error:[/bold red] {err}")
