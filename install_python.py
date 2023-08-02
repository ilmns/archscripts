#!/usr/bin/env python3

import subprocess
import os

def run(command):
    subprocess.call(command, shell=True)

def install_python():
    # Update the package lists for upgrades and new package installations
    run("sudo pacman -Sy")

    # Install Python and pip
    run("sudo pacman -S python python-pip")

def setup_python():
    # Create a .pythonrc file in the user's home directory
    pythonrc_path = os.path.expanduser("~/.pythonrc")

    # Contents of the .pythonrc file
    pythonrc_content = """
# Enable auto-completion
try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

# Enable color support for ls
try:
    import os
    os.system('')
except:
    pass
"""

    # Write the content to .pythonrc
    with open(pythonrc_path, "w") as f:
        f.write(pythonrc_content)

    # Add the .pythonrc file to the zshrc to run when a new shell opens
    zshrc_path = os.path.expanduser("~/.zshrc")

    with open(zshrc_path, "a") as f:
        f.write("\n# Python personal configurations\n")
        f.write(f"export PYTHONSTARTUP={pythonrc_path}\n")

if __name__ == "__main__":
    install_python()
    setup_python()
    print("Python installation and configuration completed.")
