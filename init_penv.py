#!/usr/bin/env python3

import os
import subprocess
import sys

def check_installed(executable):
    try:
        subprocess.run([executable, "--version"], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        return False

def main():
    if not check_installed("python3"):
        print("Python 3 is not installed. Please install Python 3 and try again.")
        sys.exit(1)

    if not check_installed("pip"):
        print("pip is not installed. Please install pip and try again.")
        sys.exit(1)

    env_name = input("Enter the name of the virtual environment (default: my_project_env): ").strip()
    if not env_name:
        env_name = "my_project_env"

    default_folder_path = os.path.join(os.path.expanduser("~"), "python_envs")
    folder_path = input(f"Enter the folder path for the virtual environment (default: {default_folder_path}): ").strip()
    if not folder_path:
        folder_path = default_folder_path

    os.makedirs(folder_path, exist_ok=True)
    env_path = os.path.join(folder_path, env_name)

    subprocess.run(["python3", "-m", "venv", env_path], check=True)

    activate_script = os.path.join(env_path, "bin", "activate")

    print(f"\nVirtual environment created at {env_path}.")
    print(f"To activate the virtual environment, run: source {activate_script}")

    print("\nUpgrading pip, setuptools, and wheel...")
    subprocess.run([os.path.join(env_path, "bin", "pip"), "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    print("\nDone! You can now install packages using pip inside your virtual environment.")

if __name__ == "__main__":
    main()
