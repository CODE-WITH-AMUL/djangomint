import os
import subprocess
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from cli.service.display import (
    print_banner, print_section_header, print_step, print_success, 
    print_error, print_info, show_project_structure, console
)
from cli.question.question import manage_django_project


def django_create():
    """Create a new Django project."""
    
    print_banner()
    print_section_header("Create New Django Project", "🚀")

    project_name = manage_django_project()

    if not project_name:
        print_error("Project name is required.")
        raise typer.Exit()

    try:
        # Show project creation steps
        steps = [
            "Initializing project structure",
            "Creating configuration files",
            "Setting up directory structure",
            "Generating default apps"
        ]
        
        for i, step in enumerate(steps, 1):
            print_step(i, step)
            import time
            time.sleep(0.3)  # Simulate progress for better UX

        console.print()  # Empty line
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"[cyan]Creating Django project '{project_name}'...", total=None)
            
            subprocess.run(
                ["django-admin", "startproject", project_name],
                check=True,
                capture_output=True
            )
            
            progress.update(task, completed=True)

        # Success message with project details
        console.print()
        success_panel = Panel(
            f"🎉 Django project [bold green]'{project_name}'[/] created successfully!\n\n"
            f"📁 Location: [bold]{os.path.join(os.getcwd(), project_name)}[/]",
            border_style="green",
            title="Success!"
        )
        console.print(success_panel)
        
        # Automatically change to the project directory
        os.chdir(project_name)
        print_info(f"Working directory: {os.getcwd()}")
        
        # Show project structure
        show_project_structure()
        
        return True

    except FileNotFoundError:
        console.print()
        error_panel = Panel(
            "django-admin not found.\n\n"
            "Please install Django first:\n"
            "[yellow]pip install django[/]",
            border_style="red",
            title="Error"
        )
        console.print(error_panel)
        return False

    except subprocess.CalledProcessError as e:
        print_error(f"Error creating project: {e}")
        return False