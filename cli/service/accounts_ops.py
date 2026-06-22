import os
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from cli.service.display import (
    print_banner, print_section_header, print_step, print_success, 
    print_warning, print_error, print_info, show_project_structure,
    print_available_commands, console
)
from cli.service.config_updater import project_name_from_path, update_settings_file, update_urls_file
from cli.question.question import create_django_app


def django_accounts():
    """Create a default accounts app with custom authentication code."""

    print_banner()
    print_section_header("Create Accounts App with Authentication", "🔐")

    app_name = "accounts"

    if not os.path.exists("manage.py"):
        print_error("manage.py not found. Run this command from the Django project root.")
        return False

    try:
        # Step 1: Create the app
        print_step(1, "Creating accounts app")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Creating Django app 'accounts'...", total=None)
            
            import subprocess
            subprocess.run(
                ["python", "manage.py", "startapp", app_name],
                check=True,
                capture_output=True
            )
            
            progress.update(task, completed=True)
        
        print_success(f"Accounts app '{app_name}' created!")

        current_dir = os.getcwd()
        app_path = os.path.join(current_dir, app_name)

        if os.path.exists(app_path):
            # Step 2: Copy custom views
            print_step(2, "Setting up custom authentication views")
            
            source_views = os.path.join(current_dir, "..", "generators", "accounts", "Basicsecuirty", "security", "views.py")
            dest_views = os.path.join(app_path, "views.py")
            
            if os.path.exists(source_views):
                shutil.copy(source_views, dest_views)
                print_success("Custom views.py installed")
            else:
                print_warning(f"Custom views.py not found at: {source_views}")
            
            # Step 3: Create custom urls
            print_step(3, "Configuring URL patterns")
            
            source_urls = os.path.join(current_dir, "..", "generators", "accounts", "Basicsecuirty", "security", "urls.py")
            dest_urls = os.path.join(app_path, "urls.py")
            
            if os.path.exists(source_urls):
                with open(source_urls, 'r') as f:
                    urls_content = f.read()
                # Replace the import to match the new app structure
                urls_content = urls_content.replace('from .security import djmint_views', 'from . import views')
                urls_content = urls_content.replace('djmint_views.', 'views.')
                with open(dest_urls, 'w') as f:
                    f.write(urls_content)
                print_success("Custom urls.py configured")
            else:
                print_warning(f"Custom urls.py not found at: {source_urls}")
            
            # Step 4: Update settings
            print_step(4, "Updating project settings")
            
            settings_file = os.path.join(current_dir, project_name_from_path(current_dir), "settings.py")
            if os.path.exists(settings_file):
                update_settings_file(settings_file)
            else:
                print_warning(f"settings.py not found at: {settings_file}")
            
            # Step 5: Update main urls
            print_step(5, "Updating main URL configuration")
            
            urls_file = os.path.join(current_dir, project_name_from_path(current_dir), "urls.py")
            if os.path.exists(urls_file):
                update_urls_file(urls_file)
            else:
                print_warning(f"urls.py not found at: {urls_file}")
            
            # Final success message
            console.print()
            success_panel = Panel(
                "🎉 [bold]Accounts app with custom authentication is ready![/]\n\n"
                "✓ All configurations have been automatically updated\n"
                "✓ Custom authentication views installed\n"
                "✓ URL patterns configured\n"
                "✓ Settings updated",
                border_style="green",
                title="Setup Complete"
            )
            console.print(success_panel)
            
            # Show available commands
            print_available_commands()
        
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"Error creating accounts app: {e}")
        return False

    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False


def django_app_create():
    """Create a Django app inside an existing project."""
    
    print_banner()
    print_section_header("Create Django App", "📱")

    app_name = create_django_app()

    if not app_name:
        print_error("App name is required.")
        return False

    if not os.path.exists("manage.py"):
        print_error("manage.py not found. Run this command from the Django project root.")
        return False

    try:
        print_info(f"Creating app: [bold]{app_name}[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"[cyan]Creating Django app '{app_name}'...", total=None)
            
            import subprocess
            subprocess.run(
                ["python", "manage.py", "startapp", app_name],
                check=True,
                capture_output=True
            )
            
            progress.update(task, completed=True)

        console.print()
        success_panel = Panel(
            f"🎉 App [bold green]'{app_name}'[/] created successfully!\n\n"
            f"📁 Location: [bold]{os.path.join(os.getcwd(), app_name)}[/]",
            border_style="green",
            title="Success!"
        )
        console.print(success_panel)
        
        # Show app structure
        print_section_header(f"App Structure: {app_name}", "📁")
        
        if os.path.exists(app_name):
            from rich.table import Table
            table = Table(show_header=False, box=None)
            table.add_column(style="bold")
            
            for item in sorted(os.listdir(app_name)):
                item_path = os.path.join(app_name, item)
                if os.path.isdir(item_path):
                    table.add_row(f"📁 {item}/")
                else:
                    table.add_row(f"📄 {item}")
            
            console.print(table)
        
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"Error creating app: {e}")
        return False