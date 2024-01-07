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

@app.command()
def disk_usage():
    """Shows disk usage statistics."""
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Device", style="dim")
    table.add_column("Mountpoint")
    table.add_column("File System Type")
    table.add_column("Total Size (GB)")
    table.add_column("Used (GB)")
    table.add_column("Free (GB)")
    table.add_column("Usage (%)", justify="right")

    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        total = usage.total / (1024 ** 3)
        used = usage.used / (1024 ** 3)
        free = usage.free / (1024 ** 3)
        percent = usage.percent

        # Color coding based on usage percentage
        if percent > 80:
            usage_color = "red"
        elif percent > 50:
            usage_color = "yellow"
        else:
            usage_color = "green"

        table.add_row(
            partition.device,
            partition.mountpoint,
            partition.fstype,
            f"{total:.2f}",
            f"{used:.2f}",
            f"{free:.2f}",
            f"[{usage_color}]{percent}%[/]"
        )

    console.print(table)


if __name__ == "__main__":
    app()
