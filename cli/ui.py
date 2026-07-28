"""Project ZERO — Rich Terminal UX Presenter (Phase 4 Capability #23).

Renders rich terminal UI elements (tree views, diff blocks, syntax highlighting, spinners, panels).
"""

from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.tree import Tree
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class RichTerminalPresenter:
    """Renders rich terminal widgets for zero-GUI command line interface."""

    @staticmethod
    def render_panel(title: str, content: str, style: str = "blue"):
        """Render a formatted rich panel."""
        console.print(Panel(content, title=title, border_style=style))

    @staticmethod
    def render_markdown(md_text: str):
        """Render GitHub flavored markdown in terminal."""
        console.print(Markdown(md_text))

    @staticmethod
    def render_code(code: str, language: str = "python"):
        """Render syntax highlighted code block."""
        console.print(Syntax(code, language, theme="monokai", line_numbers=True))

    @staticmethod
    def render_tree(root_label: str, items: List[str]):
        """Render a hierarchical tree view."""
        tree = Tree(f"[bold cyan]{root_label}[/bold cyan]")
        for item in items:
            tree.add(item)
        console.print(tree)
