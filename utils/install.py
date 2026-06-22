#-----------------[IMPORT MODULES]------------------#
import subprocess
import sys


#-----------------[INSTALL MODULES]------------------#
def install():
    try:
        print("Installing dependencies...")

        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            "requirements.txt"
        ])

        print("All dependencies installed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")