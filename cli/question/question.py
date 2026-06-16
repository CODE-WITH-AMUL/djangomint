import questionary
import time
import sys


def animation(text, time_sec=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(time_sec)
    print()


def manage_django_project():
    animation("Setting up your Django project...")

    project_name = questionary.text(
        "Write your Django project name:"
    ).ask()

    return project_name

def create_django_app():
    animation("Creating Django app...")
    app_name = questionary.text(
        "Write your Django app name:"
    ).ask()
    
    return app_name

