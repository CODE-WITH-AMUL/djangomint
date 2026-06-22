import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint
from rich.syntax import Syntax
import time

console = Console()


def print_banner():
    """Display a beautiful ASCII banner"""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║           🐍 DJANGO PROJECT BUILDER         ║
    ║              Fast & Easy CLI Tool            ║
    ╚══════════════════════════════════════════════╝
    """
    console.print(Panel(banner.strip(), border_style="bold cyan"))


def print_section_header(title, emoji="🔧"):
    """Print a formatted section header"""
    console.print(f"\n{emoji} {title}")
    console.print("─" * 50, style="dim")


def print_success(message):
    """Print a success message with checkmark"""
    console.print(f"✅ {message}", style="bold green")


def print_warning(message):
    """Print a warning message"""
    console.print(f"⚠️  {message}", style="bold yellow")


def print_error(message):
    """Print an error message"""
    console.print(f"❌ {message}", style="bold red")


def print_info(message):
    """Print an info message"""
    console.print(f"ℹ️  {message}", style="bold blue")


def print_step(step_num, message):
    """Print a step indicator"""
    console.print(f"  [{step_num}] {message}", style="cyan")


def show_progress(message, duration=1):
    """Show a progress spinner for aesthetic purposes"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]{message}...", total=None)
        time.sleep(duration)
        progress.update(task, completed=True)


def show_project_structure():
    """Display the project structure in a nice format"""
    print_section_header("Project Structure", "📁")
    
    # Show top-level files and directories
    items = os.listdir('.')
    table = Table(show_header=False, box=None)
    table.add_column(style="bold")
    
    for item in sorted(items):
        if os.path.isdir(item):
            table.add_row(f"📁 {item}/")
        else:
            table.add_row(f"📄 {item}")
    
    console.print(table)


def show_app_structure(app_name):
    """Display the app structure"""
    print_section_header(f"App Structure: {app_name}", "📁")
    
    if os.path.exists(app_name):
        table = Table(show_header=False, box=None)
        table.add_column(style="bold")
        
        for item in sorted(os.listdir(app_name)):
            item_path = os.path.join(app_name, item)
            if os.path.isdir(item_path):
                table.add_row(f"📁 {item}/")
            else:
                table.add_row(f"📄 {item}")
        
        console.print(table)


def print_available_commands():
    """Print useful commands for the user"""
    print_section_header("Quick Start Commands", "💡")
    
    commands_table = Table(show_header=False, box=None)
    commands_table.add_column(style="bold yellow")
    commands_table.add_column(style="dim")
    
    commands_table.add_row("python manage.py makemigrations", "# Create database migrations")
    commands_table.add_row("python manage.py migrate", "# Apply database migrations")
    commands_table.add_row("python manage.py runserver", "# Start development server")
    
    console.print(commands_table)


def show_project_status():
    """Show current project status panel"""
    import os
    current_dir = os.getcwd()
    project_info = Panel(
        f"📁 Current Project: [bold cyan]{os.path.basename(current_dir)}[/]\n"
        f"📂 Location: [dim]{current_dir}[/]",
        border_style="cyan",
        title="Project Status"
    )
    console.print(project_info)