from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Static, Input
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
        return Text(log.rstrip())
    
    level = log_parts[1].strip()
    return Text(log.rstrip(), style=level_colors.get(level))

class Timber(App):

    BINDINGS = [("q", "quit", "Exit the App"), ("p", "toggle_pause", "Pause/Resume")]

    def __init__(self):
        super().__init__()
        self.position = 0
        self.paused = False
        self.all_lines = []
        self.filter_text = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Filter logs...")
        yield RichLog()
        yield Static(self.get_status_text(), id="status")
        yield Footer()

    def on_mount(self):
        self.read_new_lines()
        self.set_interval(0.2, self.read_new_lines)


    def read_new_lines(self):
        if self.paused:
            return

        rich_log = self.query_one(RichLog)
        at_bottom = rich_log.scroll_y >= rich_log.max_scroll_y - 1

        with open("app.log", "r") as file:
            file.seek(self.position)
            while True:
                log = file.readline()

                if log == "":
                    break

                if self.matches_filter(log):
                    parsed_log = style_log_line(log)
                    rich_log.write(parsed_log, scroll_end=at_bottom)
                self.all_lines.append(log.rstrip())

            self.position = file.tell()

    def action_toggle_pause(self):
        self.paused = not self.paused
        self.update_status()


    def update_status(self):
        status = self.query_one("#status", Static)
        status.update(self.get_status_text())

    def get_status_text(self):
        return "[yellow]● PAUSED[/yellow]" if self.paused else "[green]● RUNNING[/green]"

    
    def on_input_changed(self, event: Input.Changed):
        rich_log = self.query_one(RichLog)
        rich_log.clear()
        self.filter_text = event.value

        for log in self.all_lines:
            if self.matches_filter(log):
                styled_log = style_log_line(log)
                rich_log.write(styled_log)

    def matches_filter(self, log):
        return self.filter_text.lower() in log.lower()
        


if __name__ == "__main__":
    app = Timber()
    app.run()
