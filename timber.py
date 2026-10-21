from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog

class Timber(App):

    BINDINGS = [("q", "quit", "Exit the App")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog()
        yield Footer()


if __name__ == "__main__":
    app = Timber()
    app.run()
