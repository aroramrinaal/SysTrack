import typer
import psutil
import platform

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

@app.command()
def network_stats():
    """Displays network statistics."""
    net_io = psutil.net_io_counters()
    interfaces = psutil.net_if_addrs()

    console = Console()
    net_table = Table(show_header=True, header_style="bold cyan")
    net_table.add_column("Metric")
    net_table.add_column("Value", justify="right")

    net_table.add_row("Bytes Sent", f"{net_io.bytes_sent / (1024 ** 2):.2f} MB")
    net_table.add_row("Bytes Received", f"{net_io.bytes_recv / (1024 ** 2):.2f} MB")
    net_table.add_row("Packets Sent", str(net_io.packets_sent))
    net_table.add_row("Packets Received", str(net_io.packets_recv))

    console.print("Network IO:", style="bold underline")
    console.print(net_table)

    for iface, addrs in interfaces.items():
        iface_table = Table(show_header=True, header_style="bold green")
        iface_table.add_column("Interface", style="dim")
        iface_table.add_column("Address")
        iface_table.add_column("Netmask")
        iface_table.add_column("Broadcast", justify="right")

        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                # This is the MAC address
                iface_table.add_row(iface, "MAC", addr.address, "")
            else:
                # IP addresses
                iface_table.add_row(iface, addr.address, addr.netmask, addr.broadcast or "")

        console.print(f"Interface: {iface}", style="bold underline")
        console.print(iface_table)

@app.command()
def system_info():
    """Displays general system information."""
    console = Console()
    info_table = Table(show_header=True, header_style="bold blue")
    info_table.add_column("Category", style="dim")
    info_table.add_column("Value", justify="right")

    # System information
    info_table.add_row("OS", platform.system())
    info_table.add_row("OS Version", platform.version())
    info_table.add_row("OS Release", platform.release())
    info_table.add_row("Architecture", platform.architecture()[0])
    info_table.add_row("Hostname", platform.node())
    info_table.add_row("Uptime", format_uptime(psutil.boot_time()))

    console.print("System Information:", style="bold underline")
    console.print(info_table)

def format_uptime(boot_time):
    """Formats system uptime."""
    uptime_seconds = psutil.time.time() - boot_time
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

if __name__ == "__main__":
    app()
