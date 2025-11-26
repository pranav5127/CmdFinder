from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual import on
from textual.widgets import Header, Input, ListView, Label, ListItem

class CmdHistoryApp(App):
    TITLE = "CmdHistory"
    SUB_TITLE = "A Tool to easily search previously executed commands in the terminal."
    CSS_PATH = "app.tcss"

    # stores history for the current command
    history: list[str] = reactive([], layout=False)
    full_history = list[str] = []
    # current keyword
    search_keyword = reactive(str)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="🔎 Ctrl+k", id="search")
        self.list_view = ListView()
        yield self.list_view

    def on_mount(self) -> None:
        #Load full history at startup
        self.full_history = self.load_history()
        # Initially show the last 50 commands
        self.items = list(reversed(self.full_history[-50:]))


    def add_new_item(self) -> None:
        self.items = [*self.items, f"Item {len(self.items)+1}"]

    def watch_items(self, new: list[str]) -> None:
        self.list_view.clear()
        for item in new:
            self.list_view.append(ListItem(Label(item)))

    @on(Input.Changed, "#search")
    def update_list_items(self, event: Input.Changed) -> None:
        self.search_keyword = event.value

if __name__ == "__main__":
    app = CmdHistoryApp().run()