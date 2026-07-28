"""Project ZERO — Interactive Terminal REPL Subsystem."""

import sys
import asyncio
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from brain.brain import Brain
from voice.manager import VoiceManager
from voice.listener import ActiveListener
from zero_logging import logger

console = Console()


class ZeroShell:
    """Thin interactive CLI shell delegating input processing to Brain & VoiceManager."""

    def __init__(self, brain: Optional[Brain] = None, voice_manager: Optional[VoiceManager] = None):
        self.brain = brain or Brain()
        self.voice_manager = voice_manager or VoiceManager()
        self.active_listener = ActiveListener(
            brain=self.brain,
            stt_provider=self.voice_manager.stt_provider,
            tts_provider=self.voice_manager.tts_provider
        )

    def print_welcome(self):
        """Display ZERO v0.1 welcome header banner."""
        banner = (
            "[bold blue]ZERO v0.1[/bold blue] — Personal Autonomous Intelligence Platform\n"
            "[dim]Python-First Core Infrastructure • Voice & Active Listening Phase 3A • Type 'help' for commands • 'exit' to quit[/dim]"
        )
        console.print(Panel(banner, border_style="blue", title="[bold white]Project ZERO[/bold white]"))

    def print_help(self):
        """Display help command table."""
        table = Table(title="Project ZERO Commands", border_style="dim")
        table.add_column("Command / Intent", style="bold cyan", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("listen", "Start active voice listening loop")
        table.add_row("mute", "Mute voice Text-to-Speech playback")
        table.add_row("unmute", "Unmute voice Text-to-Speech playback")
        table.add_row("voices", "List available TTS voice models")
        table.add_row("microphones", "List connected microphone input devices")
        table.add_row("speaker", "List connected speaker output devices")
        table.add_row("voice settings", "Inspect voice configuration settings")
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

    async def cmd_listen(self):
        """Start active voice listening conversation loop."""
        console.print("\n[bold green]Active Voice Listening Started...[/bold green] (Speak now or say 'stop listening')\n")
        
        def on_speech(user_text: str):
            console.print(f"[bold cyan]User (Voice):[/bold cyan] {user_text}")

        def on_response(zero_text: str):
            console.print(f"[bold blue]ZERO (Voice):[/bold blue] {zero_text}\n")

        try:
            await self.active_listener.start_listening_loop(on_user_speech=on_speech, on_zero_response=on_response)
        except Exception as err:
            console.print(f"[bold red]Voice loop error:[/bold red] {err}")
        finally:
            console.print("[dim]Active voice listening ended.[/dim]\n")

    def cmd_mute(self):
        """Mute voice output."""
        self.active_listener.mute()
        console.print("[bold yellow]Voice output MUTED.[/bold yellow]")

    def cmd_unmute(self):
        """Unmute voice output."""
        self.active_listener.unmute()
        console.print("[bold green]Voice output UNMUTED.[/bold green]")

    def cmd_voices(self):
        """Display available TTS voices."""
        voices = self.voice_manager.list_voices()
        table = Table(title=f"Available TTS Voices ({len(voices)})", border_style="magenta")
        table.add_column("Voice ID", style="bold cyan")
        table.add_column("Voice Name", style="white")
        table.add_column("Languages", style="dim")

        for v in voices:
            table.add_row(v.id, v.name, ", ".join(v.languages))

        console.print(table)

    def cmd_microphones(self):
        """Display connected input audio devices."""
        mics = self.voice_manager.list_microphones()
        table = Table(title=f"Input Microphones ({len(mics)})", border_style="cyan")
        table.add_column("ID", style="bold cyan")
        table.add_column("Device Name", style="white")
        table.add_column("Channels", style="dim")
        table.add_column("Default", style="bold yellow")

        for m in mics:
            table.add_row(str(m.id), m.name, str(m.max_input_channels), "Yes" if m.is_default else "No")

        console.print(table)

    def cmd_speaker(self):
        """Display connected output audio devices."""
        spks = self.voice_manager.list_speakers()
        table = Table(title=f"Output Speakers ({len(spks)})", border_style="green")
        table.add_column("ID", style="bold cyan")
        table.add_column("Device Name", style="white")
        table.add_column("Channels", style="dim")
        table.add_column("Default", style="bold yellow")

        for s in spks:
            table.add_row(str(s.id), s.name, str(s.max_output_channels), "Yes" if s.is_default else "No")

        console.print(table)

    def cmd_voice_settings(self):
        """Inspect voice settings configuration."""
        s = self.brain.settings
        table = Table(title="Voice Settings Configuration", border_style="blue")
        table.add_column("Setting", style="bold cyan")
        table.add_column("Value", style="bold white")

        table.add_row("VOICE_ENABLED", str(s.voice_enabled))
        table.add_row("TTS_PROVIDER", s.tts_provider)
        table.add_row("STT_PROVIDER", s.stt_provider)
        table.add_row("VOICE_NAME", s.voice_name)
        table.add_row("LANGUAGE", s.language)
        table.add_row("MICROPHONE_DEVICE", s.microphone_device or "Default")
        table.add_row("SPEAKER_DEVICE", s.speaker_device or "Default")
        table.add_row("MUTED", "Yes" if self.active_listener.muted else "No")

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
        table.add_row("VOICE_ENABLED", str(s.voice_enabled))
        table.add_row("TTS_PROVIDER", s.tts_provider)
        table.add_row("STT_PROVIDER", s.stt_provider)

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

        # Optionally speak response if voice is unmuted (non-blocking task)
        complete_response = "".join(full_text)
        if not self.active_listener.muted and complete_response:
            try:
                asyncio.create_task(self.voice_manager.tts_provider.speak(complete_response))
            except Exception:
                pass

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
                elif cmd_lower == "listen":
                    await self.cmd_listen()
                elif cmd_lower == "mute":
                    self.cmd_mute()
                elif cmd_lower == "unmute":
                    self.cmd_unmute()
                elif cmd_lower == "voices":
                    self.cmd_voices()
                elif cmd_lower == "microphones":
                    self.cmd_microphones()
                elif cmd_lower == "speaker":
                    self.cmd_speaker()
                elif cmd_lower == "voice settings":
                    self.cmd_voice_settings()
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
