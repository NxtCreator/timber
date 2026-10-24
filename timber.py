import argparse
import sys
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog, Static, Input
from textual.binding import Binding
from rich.text import Text

parser = argparse.ArgumentParser(description="Timber - A terminal log viewer")
parser.add_argument('file_path')
args = parser.parse_args()

file_path = Path(args.file_path)

if not file_path.is_file():
    print(f"Error: The path {file_path} does not exist. Please check the path and try again")
    sys.exit(1)

level_colors = {
    "INFO": "green",
    "WARN": "yellow",
    "ERROR": "red",
    "DEBUG": "dim cyan",
    "CRITICAL": "bold red"
}

def style_log_line(log):
    level = get_level(log)
    if level is None:
        return Text(log.rstrip())
    return Text(log.rstrip(), style=level_colors[level])


def get_level(log):
    log_line_parts = log.split("|")

    if len(log_line_parts) >= 3:
        log_level = log_line_parts[1].strip()
        if log_level in level_colors:
            return log_level
    return None

class Timber(App):

    BINDINGS = [("q", "quit", "Exit the App"), 
                ("p", "toggle_pause", "Pause/Resume"),
                ("/", "focus_filter", "Focus the Filter"),
                ("escape", "focus_log_viewer", "Focus Log Viewer"),
                Binding("1", "toggle_level('INFO')", "Toggle INFO", show=False),
                Binding("2", "toggle_level('WARN')", "Toggle WARN", show=False),
                Binding("3", "toggle_level('ERROR')", "Toggle ERROR", show=False),
                Binding("4", "toggle_level('DEBUG')", "Toggle DEBUG", show=False),
                Binding("5", "toggle_level('CRITICAL')", "Toggle CRITICAL", show=False),]

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.position = 0
        self.paused = False
        self.all_lines = []
        self.filter_text = ""
        self.enabled_levels = set(level_colors)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Filter logs...")
        yield RichLog()
        yield Static(self.get_status_text(), id="status")
        yield Footer()

    def on_mount(self):
        self.query_one(RichLog).focus()
        self.read_new_lines()
        self.set_interval(0.2, self.read_new_lines)


    def read_new_lines(self):
        if self.paused:
            return

        rich_log = self.query_one(RichLog)
        at_bottom = rich_log.scroll_y >= rich_log.max_scroll_y - 1

        with open(self.filename, "r") as file:
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
        level_labels = []

        for level in level_colors:
            if level in self.enabled_levels:
                level_labels.append(level)
            else:
                level_labels.append(f"[dim]{level}[/dim]")

        levels_text = " | ".join(level_labels)
        status = "[yellow]● PAUSED[/yellow]" if self.paused else "[green]● RUNNING[/green]"

        return f"{status} | {levels_text}"

    
    def on_input_changed(self, event: Input.Changed):
        self.filter_text = event.value
        self.refresh_logs()


    def matches_filter(self, log):
        level = get_level(log)
        matches_search = self.filter_text.lower() in log.lower()
        level_enabled = level in self.enabled_levels
        is_unknown = level is None
        return matches_search and (level_enabled or is_unknown)

    def action_focus_filter(self):
        filter_input = self.query_one(Input)
        self.set_focus(filter_input)

    def action_focus_log_viewer(self):
        log_viewer = self.query_one(RichLog)
        self.set_focus(log_viewer)

    def action_toggle_level(self, level: str):
        if level in self.enabled_levels:
            self.enabled_levels.discard(level)
        else: 
            self.enabled_levels.add(level)
        self.refresh_logs()
        self.update_status()

    def refresh_logs(self):
        rich_log = self.query_one(RichLog)
        rich_log.clear()

        for log in self.all_lines:
            if self.matches_filter(log):
                styled_log = style_log_line(log)
                rich_log.write(styled_log)
        


if __name__ == "__main__":
    app = Timber(args.file_path)
    app.run()
