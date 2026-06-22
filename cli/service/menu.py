import os
import subprocess
import questionary
from questionary import Style
from cli.service.display import print_banner, show_project_status, console, print_info
from cli.service.project_ops import django_create
from cli.service.accounts_ops import django_accounts, django_app_create


def show_main_menu():
    """Show interactive menu when main.py runs without arguments"""
    
    custom_style = Style([
        ('qmark', 'fg:#673ab7 bold'),
        ('question', 'bold'),
        ('answer', 'fg:#f44336 bold'),
        ('pointer', 'fg:#673ab7 bold'),
        ('highlighted', 'fg:#673ab7 bold'),
        ('selected', 'fg:#cc5454'),
    ])
    
    while True:
        console.clear()
        print_banner()
        
        choice = questionary.select(
            "🚀 What would you like to do?",
            choices=[
                questionary.Choice("Create a new Django project", "create_project"),
                questionary.Choice("Create a Django app (inside existing project)", "create_app"),
                questionary.Choice("Create accounts app (inside existing project)", "create_accounts"),
                questionary.Separator(),
                questionary.Choice("Exit", "exit"),
            ],
            style=custom_style
        ).ask()
        
        console.clear()
        
        if choice == "create_project":
            django_create()
            if os.path.exists("manage.py"):
                show_project_menu()
        elif choice == "create_app":
            if not os.path.exists("manage.py"):
                console.print("\n❌ Error: manage.py not found. Please run this from a Django project directory.\n")
            else:
                django_app_create()
                show_project_menu()
        elif choice == "create_accounts":
            if not os.path.exists("manage.py"):
                console.print("\n❌ Error: manage.py not found. Please run this from a Django project directory.\n")
            else:
                django_accounts()
                show_project_menu()
        elif choice == "exit":
            console.print("\n👋 [bold green]Goodbye! Happy coding![/]\n")
            break


def show_project_menu():
    """Show menu for actions inside a Django project"""
    
    custom_style = Style([
        ('qmark', 'fg:#673ab7 bold'),
        ('question', 'bold'),
        ('answer', 'fg:#f44336 bold'),
        ('pointer', 'fg:#673ab7 bold'),
        ('highlighted', 'fg:#673ab7 bold'),
        ('selected', 'fg:#cc5454'),
    ])
    
    while True:
        # Show current project status
        show_project_status()
        
        choice = questionary.select(
            "🔧 What would you like to do next?",
            choices=[
                questionary.Choice("📱 Create a Django app", "create_app"),
                questionary.Choice("🔐 Create accounts app", "create_accounts"),
                questionary.Choice("🏃 Run development server", "runserver"),
                questionary.Separator(),
                questionary.Choice("↩️  Return to main menu", "main_menu"),
                questionary.Choice("❌ Exit", "exit"),
            ],
            style=custom_style
        ).ask()
        
        if choice == "create_app":
            django_app_create()
        elif choice == "create_accounts":
            django_accounts()
        elif choice == "runserver":
            print_info("Starting development server...")
            try:
                subprocess.run(["python", "manage.py", "runserver"])
            except KeyboardInterrupt:
                console.print("\n⏹️  Server stopped.")
        elif choice == "main_menu":
            show_main_menu()
            break
        elif choice == "exit":
            console.print("\n👋 [bold green]Goodbye! Happy coding![/]\n")
            import sys
            sys.exit()