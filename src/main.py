import typer
import psutil

app = typer.Typer()

@app.command()
def welcome():
    """Displays a welcome message."""
    typer.echo("Welcome to SysTrack! Your system stats monitor.")

@app.command()
def cpu_usage():
    """Shows the current CPU usage."""
    usage = psutil.cpu_percent(interval=1)
    typer.echo(f"Current CPU Usage: {usage}%")

@app.command()
def memory_usage():
    """Shows the current memory usage."""
    memory = psutil.virtual_memory()
    total = memory.total / (1024 ** 3)  # Convert to GB
    used = memory.used / (1024 ** 3)
    available = memory.available / (1024 ** 3)
    typer.echo(f"Total Memory: {total:.2f} GB")
    typer.echo(f"Used Memory: {used:.2f} GB")
    typer.echo(f"Available Memory: {available:.2f} GB")


if __name__ == "__main__":
    app()
