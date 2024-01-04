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

if __name__ == "__main__":
    app()
