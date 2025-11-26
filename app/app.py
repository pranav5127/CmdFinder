from textual.app import App, ComposeResult
from textual.widgets import Header, Input

class CmdHistoryApp(App):
    TITLE = "CmdHistory"
    SUB_TITLE = "A Tool to easily search previously executed commands in the terminal."
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="🔎 Ctrl+k", id="search")

if __name__ == "__main__":
    app = CmdHistoryApp().run()