from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from rich.text import Text

level_colors = {
    "INFO": "green",
    "WARN": "yellow",
    "ERROR": "red",
    "DEBUG": "dim cyan",
    "CRITICAL": "bold red"
}

def style_log_line(log):
    log_parts = log.split("|")
    if len(log_parts) < 3:
        return Text(log.rstrip(), style="white")
    
    level = log_parts[1].strip()
    return Text(log.rstrip(), style=level_colors.get(level, "white"))

class Timber(App):

    BINDINGS = [("q", "quit", "Exit the App")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog()
        yield Footer()

    def on_mount(self):
        rich_log = self.query_one(RichLog)

        with open('app.log', 'r') as file:
            while True:
                log = file.readline()
                
                if log == "":
                    break

                parsed_log = style_log_line(log)
                rich_log.write(parsed_log)

            self.position = file.tell()
        self.set_interval(1, self.check_new_logs)

    def check_new_logs(self):
        rich_log = self.query_one(RichLog)
        with open("app.log", "r") as file:
            file.seek(self.position)
            while True:
                log = file.readline()

                if log == "":
                    break

                parsed_log = style_log_line(log)
                rich_log.write(parsed_log)

            self.position = file.tell()
            


if __name__ == "__main__":
    app = Timber()
    app.run()
