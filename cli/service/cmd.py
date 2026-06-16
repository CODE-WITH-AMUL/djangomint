import typer
import subprocess
from cli.question.question import manage_django_project, create_django_app

app = typer.Typer()


@app.command()
def django_create():
    project_name = manage_django_project()

    if not project_name:
        typer.echo("Project name is required.")
        raise typer.Exit()

    typer.echo(f"Creating project: {project_name}")

    try:
        subprocess.run(
            ["django-admin", "startproject", project_name],
            check=True
        )

        typer.echo(
            f" Django project '{project_name}' created successfully!"
        )

    except FileNotFoundError:
        typer.echo(
            " django-admin not found. Install Django first."
        )
        
        try:
            import os
            os.system("pip install django")
            
        except ModuleNotFoundError:
            typer.echo(" pip is not installed. Please install pip and try again.")
            raise typer.Exit()

    except subprocess.CalledProcessError as e:
        typer.echo(f" Error: {e}")


def django_app_create():
    app_name = create_django_app()
    
    
    try:
        import os
        os.system(f"python manage.py startapp {app_name}")
    except Exception as e:
        typer.echo(f" Error: {e}")
        
        
    current_dir = os.getcwd()
    
    print(f"Current directory: {current_dir}")
    
    new_django_file_path = os.path.join(current_dir, app_name)
    os.chdir(new_django_file_path)

    if app_name:
        typer.echo(f"Creating the app : {app_name}")



if __name__ == "__main__":
    app()