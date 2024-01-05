import typer
import psutil

from rich.console import Console
from rich.table import Table

app = typer.Typer()

@app.command()
def welcome():
    """Displays a welcome message."""
    typer.echo("Welcome to SysTrack! Your system stats monitor.")

@app.command()
def cpu_usage():
    """Shows the current CPU usage."""
    usage = psutil.cpu_percent(interval=1)

    table = Table(title="CPU Usage", show_header=True, header_style="bold blue")
    table.add_column("Metric", style="dim", width=12)
    table.add_column("Percentage")

    table.add_row("Usage", f"{usage}%")

    console = Console()
    console.print(table)

@app.command()
def memory_usage():
    """Shows the current memory usage."""
    memory = psutil.virtual_memory()
    total = memory.total / (1024 ** 3)  # Convert to GB
    used = memory.used / (1024 ** 3)
    available = memory.available / (1024 ** 3)

    table = Table(title="Memory Usage", show_header=True, header_style="bold green")
    table.add_column("Type", style="dim", width=12)
    table.add_column("Size (GB)")

    table.add_row("Total", f"{total:.2f} GB")
    table.add_row("Used", f"{used:.2f} GB")
    table.add_row("Available", f"{available:.2f} GB")

    console = Console()
    console.print(table)



if __name__ == "__main__":
    app()
