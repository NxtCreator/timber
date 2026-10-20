from rich.console import Console

console = Console()


level_colors = {
    "INFO": "green",
    "WARN": "yellow",
    "ERROR": "red",
    "DEBUG": "dim cyan",
    "CRITICAL": "bold red"
}

with open("app.log", "r") as file:
    for line in file:
        level = None
        parts = line.split('|')
        if len(parts) < 3:
            console.print(line.rstrip(), style="white", markup=False)
            continue
        level = parts[1].strip()
        console.print(line.rstrip(), style=level_colors.get(level, "white"), markup=False)
          