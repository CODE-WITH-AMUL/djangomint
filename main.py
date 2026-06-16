import time
import sys

from cli.service.cmd import app


logo = r"""
______ _                        ___  ________ _   _ _____
|  _  (_)                       |  \/  |_   _| \ | |_   _|
| | | |_  __ _ _ __   __ _  ___ | .  . | | | |  \| | | |
| | | | |/ _` | '_ \ / _` |/ _ \| |\/| | | | | . ` | | |
| |/ /| | (_| | | | | (_| | (_) | |  | |_| |_| |\  | | |
|___/ |_|\__,_|_| |_|\__, |\___/\_|  |_/\___/\_| \_/ \_/
                       __/ |
                      |___/
"""


def banner():
    print(logo)


def animation(text, time_sec=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(time_sec)
    print()


def main():
    banner()
    animation("Welcome to DjangoMint CLI")
    animation("Your one-stop solution for Django setup!")

    app()   # <-- THIS runs Typer CLI


if __name__ == "__main__":
    main()