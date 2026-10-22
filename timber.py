from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Static
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
    return Text(log.rstrip(), style=level_colors.get(level))

class Timber(App):

    BINDINGS = [("q", "quit", "Exit the App"), ("p", "toggle_pause", "Pause/Resume")]

    def __init__(self):
        super().__init__()
        self.position = 0
        self.paused = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog()
        yield Static("[green]● RUNNING[/green]", id="status")
        yield Footer()

    def on_mount(self):
        self.read_new_lines()
        self.set_interval(0.2, self.read_new_lines)


    def read_new_lines(self):
        rich_log = self.query_one(RichLog)
        at_bottom = rich_log.scroll_y == rich_log.max_scroll_y

        if self.paused:
            return
        
        with open("app.log", "r") as file:
            file.seek(self.position)
            while True:
                log = file.readline()

                if log == "":
                    break

                parsed_log = style_log_line(log)
                rich_log.write(parsed_log, scroll_end=at_bottom)

            self.position = file.tell()

    def action_toggle_pause(self):
        self.paused = not self.paused
        self.update_status()


    def update_status(self):
        status = self.query_one("#status", Static)

        if self.paused:
            status.update("[yellow]● PAUSED[/yellow]")
        else:
            status.update("[green]● RUNNING[/green]")
            


if __name__ == "__main__":
    app = Timber()
    app.run()
