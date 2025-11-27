import os
import subprocess
import sys
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
        ("q", "quit", "Quit"),
    ]

    # Visible entries in the UI
    items: list[HistoryEntry] = reactive([], layout=False)

    search_keyword: str = ""
    show_timestamps: bool = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="🔎 Type to search…", id="search")
        self.list_view = ListView(id="history-list")
        yield self.list_view
        yield Footer()

    def on_mount(self) -> None:
        """Initial load from DB and focus search box."""
        # Load latest commands directly from DB
        self.items = load_history(limit=50)

        # Focus the search box by default
        search = self.query_one("#search", Input)
        self.set_focus(search)

    # ---------- Formatting & rendering ----------

    def format_entry(self, entry: HistoryEntry) -> str:
        if self.show_timestamps and entry.timestamp is not None:
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
                ListItem(
                    Label(self.format_entry(entry), markup=False)
                )
            )

    def watch_items(self, items: list[HistoryEntry]) -> None:
        self.refresh_items_view()

    def watch_show_timestamps(self, show: bool) -> None:
        self.refresh_items_view()

    # ---------- Search ----------

    @on(Input.Changed, "#search")
    def update_list_items(self, event: Input.Changed) -> None:
        self.search_keyword = event.value
        self.items = fuzzy_search(self.search_keyword, limit=50)

    # ---------- Enter selects command ----------

    @on(ListView.Selected, "#history-list")
    def on_item_selected(self, event: ListView.Selected) -> None:
        index = event.index
        if 0 <= index < len(self.items):
            cmd = self.items[index].command
            self.exit(cmd)
        else:
            self.exit(None)

    # ---------- Key actions ----------

    def action_focus_list(self) -> None:
        """Focus history list."""
        self.set_focus(self.list_view)

    def action_focus_search(self) -> None:
        """Focus search input."""
        search = self.query_one("#search", Input)
        self.set_focus(search)

    def action_cursor_down(self) -> None:
        """Move down."""
        self.list_view.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Move up."""
        self.list_view.action_cursor_up()

    def action_toggle_timestamps(self) -> None:
        self.show_timestamps = not self.show_timestamps


def initialize_if_needed():
    """Checks if DB exists. If not, initializes tables and imports history."""
    if not DB_PATH.exists():
        logger.info(" First run detected. Initializing database...", file=sys.stderr)
        init_db()
        logger.info(" Importing existing shell history...", file=sys.stderr)

        try:
            insert_commands_in_db()
            print("Initialization complete.", file=sys.stderr)
        except Exception as e:
            print(f"Error importing history: {e}", file=sys.stderr)


# ---------- Entry Point for Package ----------

def main() -> None:
    initialize_if_needed()

    selected_cmd = CmdHistoryApp().run()

    if selected_cmd:
        shell = os.environ.get("SHELL", "/bin/sh")
        print(f"$ {selected_cmd}")
        subprocess.run([shell, "-lc", selected_cmd])


if __name__ == "__main__":
    main()
