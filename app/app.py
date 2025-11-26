from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Input


class CmdHistoryApp(App):
    TITLE = "CmdHistory"
    SUB_TITLE = "A Tool to easily search previously executed commands in the terminal."

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="type here")

if __name__ == "__main__":
    app = CmdHistoryApp().run()