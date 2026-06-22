import questionary
import time
import sys


def animation(text, time_sec=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(time_sec)
    print()


def django_accounts():
    animation("Setting up your Django accounts...")
    
    
    options = [
        'Simple Authentication',
        'Advanced Authentication',
    ]
    
    choice = questionary.select(
        "Choose the type of authentication you want to implement:",
        choices=options
    ).ask()
    
    if choice == 'Simple Authentication':
        animation("Setting up simple authentication...")
        simple_auth()
    elif choice == 'Advanced Authentication':
        animation("Setting up advanced authentication...")
        print('We are working on this ')
        
        
from pathlib import Path
import shutil
import typer
import subprocess


def simple_auth():
    """
    Create accounts app and copy authentication templates.
    """

    project_root = Path.cwd()

    manage_py = project_root / "manage.py"

    if not manage_py.exists():
        typer.echo(" manage.py not found.")
        return

    app_name = "accounts"

    typer.echo(" Creating accounts app...")

    try:
        subprocess.run(
            ["python", "manage.py", "startapp", app_name],
            check=True
        )

    except subprocess.CalledProcessError:
        typer.echo(" Failed to create accounts app.")
        return

    accounts_dir = project_root / app_name

    current_file = Path(__file__).resolve()

    template_dir = (
        current_file.parent
        / "Basicsecuirty"
        / "security"
    )

    try:
        shutil.copy(
            template_dir / "views.py",
            accounts_dir / "views.py"
        )

        shutil.copy(
            template_dir / "urls.py",
            accounts_dir / "urls.py"
        )

        templates_source = template_dir / "templates"
        templates_destination = accounts_dir / "templates"

        if templates_source.exists():
            shutil.copytree(
                templates_source,
                templates_destination,
                dirs_exist_ok=True
            )

        typer.echo(" Authentication files copied successfully.")

    except Exception as e:
        typer.echo(f" Copy Error: {e}")
        return

    typer.echo(" Accounts module installed successfully.")