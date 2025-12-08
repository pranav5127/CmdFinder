import os
import subprocess
import sys
import shutil
from typing import Optional

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual import on
from textual.widgets import Header, Input, ListView, Label, ListItem, Footer

from cmdfinder.config.config import DB_PATH
from cmdfinder.db.db import init_db
from cmdfinder.db.insert_command import insert_commands_in_db
from cmdfinder.history import load_history, fuzzy_search, HistoryEntry
from cmdfinder.utils.logger import logger


# ----------------- Clipboard helper -----------------

def copy_to_clipboard(text: str) -> None:
    """Copy text to the system clipboard using common system tools."""
    try:
        if sys.platform.startswith("darwin"):
            # macOS
            proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            proc.communicate(input=text.encode("utf-8"))

        elif sys.platform.startswith("linux"):
            # Gnu/Linux
            if shutil.which("wl-copy"):
                proc = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
                proc.communicate(input=text.encode("utf-8"))
            elif shutil.which("xclip"):
                proc = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
                )
                proc.communicate(input=text.encode("utf-8"))
            else:
                logger.warning(
                    "No clipboard tool found (install wl-clipboard or xclip) – "
                    "cannot copy to clipboard."
                )

        elif sys.platform.startswith("win"):
            # Windows
            proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            proc.communicate(input=text.encode("utf-16le"))

        else:
            logger.warning(f"Clipboard unsupported on platform: {sys.platform}")

    except Exception as e:
        logger.error(f"Clipboard error: {e}")


# ----------------- Main TUI App -----------------

class CmdHistoryApp(App[Optional[str]]):
    TITLE = "cmdfinder"
    SUB_TITLE = "Search your shell history"
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("ctrl+l", "focus_list", "Focus list"),
        ("l", "focus_list", "Focus list"),
        ("ctrl+s", "focus_search", "Focus search"),
        ("j", "cursor_down", "Move down"),
        ("k", "cursor_up", "Move up"),
        ("t", "toggle_timestamps", "Toggle timestamps"),
        ("ctrl+c", "copy_command", "Copy command"),
        ("q", "quit", "Quit"),
    ]

    list_view: ListView

    items: list[HistoryEntry] = reactive([], layout=False)

    search_keyword: str = ""
    show_timestamps: bool = reactive(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define list_view in __init__ so linters don't complain
        self.list_view = ListView(id="history-list")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="🔎 Type to search…", id="search")
        yield self.list_view
        yield Footer()

    def on_mount(self) -> None:
        """Initial DB load & focus."""
        self.items = load_history(limit=50)

        search = self.query_one("#search", Input)
        self.set_focus(search)

    # ------------ Formatting & rendering ------------

    def format_entry(self, entry: HistoryEntry) -> str:
        if self.show_timestamps and entry.timestamp:
            ts = entry.timestamp.strftime("%d %b %Y %H:%M")
            return f"[{ts}]  {entry.command}"
        return entry.command

    def refresh_items_view(self) -> None:
        self.list_view.clear()

        if not self.items:
            self.list_view.append(
                ListItem(Label("(no history found)", markup=False))
            )
            return

        for entry in self.items:
            self.list_view.append(
                ListItem(Label(self.format_entry(entry), markup=False))
            )

    def watch_items(self, items: list[HistoryEntry]) -> None:
        self.refresh_items_view()

    def watch_show_timestamps(self, show: bool) -> None:
        self.refresh_items_view()

    # ------------ Search ------------

    @on(Input.Changed, "#search")
    def update_list_items(self, event: Input.Changed) -> None:
        self.search_keyword = event.value
        self.items = fuzzy_search(self.search_keyword, limit=50)

    # ------------ Select with Enter ------------

    @on(ListView.Selected, "#history-list")
    def on_item_selected(self, event: ListView.Selected) -> None:
        index = event.index
        if 0 <= index < len(self.items):
            cmd = self.items[index].command
            self.exit(cmd)
        else:
            self.exit(None)

    # ------------ Key actions ------------

    def action_focus_list(self) -> None:
        self.set_focus(self.list_view)

    def action_focus_search(self) -> None:
        search = self.query_one("#search", Input)
        self.set_focus(search)

    def action_cursor_down(self) -> None:
        self.list_view.action_cursor_down()

    def action_cursor_up(self) -> None:
        self.list_view.action_cursor_up()

    def action_toggle_timestamps(self) -> None:
        self.show_timestamps = not self.show_timestamps

    # ------------ Ctrl+C Copy ------------

    def action_copy_command(self) -> None:
        """Copy the currently selected command to clipboard using Ctrl+C."""
        if self.screen.focused is not self.list_view:
            return

        index = getattr(self.list_view, "index", None)
        if index is None or index < 0 or index >= len(self.items):
            return

        cmd = self.items[index].command
        copy_to_clipboard(cmd)

        try:
            self.notify(f"Copied: {cmd}", timeout=1.3)
        except Exception:
            pass


# ----------------- Initialization -----------------

def initialize_if_needed():
    """Initialize DB on first run."""
    if not DB_PATH.exists():
        logger.info(" First run detected. Initializing database...", file=sys.stderr)
        init_db()
        logger.info(" Importing existing shell history...", file=sys.stderr)

        try:
            insert_commands_in_db()
            print("Initialization complete.", file=sys.stderr)
        except Exception as e:
            print(f"Error importing history: {e}", file=sys.stderr)


# ----------------- Entry point -----------------

def main() -> None:
    initialize_if_needed()

    selected_cmd = CmdHistoryApp().run()

    if selected_cmd:
        shell = os.environ.get("SHELL", "/bin/sh")
        print(f"$ {selected_cmd}")
        subprocess.run([shell, "-lc", selected_cmd])


if __name__ == "__main__":
    main()
