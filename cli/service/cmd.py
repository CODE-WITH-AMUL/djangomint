import os
import typer
from cli.service.project_ops import django_create
from cli.service.accounts_ops import django_accounts, django_app_create
from cli.service.menu import show_main_menu, show_project_menu

app = typer.Typer()


@app.command()
def django_create_command():
    """Create a new Django project."""
    django_create()


@app.command()
def django_app_create_command():
    """Create a Django app inside an existing project."""
    django_app_create()


@app.command()
def django_accounts_command():
    """Create a default accounts app with custom authentication code."""
    django_accounts()


def main_app():
    """Main entry point that can be called from main.py"""
    import sys
    
    # Check if we have command line arguments
    if len(sys.argv) == 1:
        show_main_menu()
    else:
        # Otherwise use normal typer CLI
        app()


if __name__ == "__main__":
    main_app()