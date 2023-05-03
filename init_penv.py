#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

def is_executable_installed(executable):
    try:
        subprocess.run([executable, "--version"], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        return False

def search_existing_envs(folder_path):
    envs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    return envs

def create_requirements_file(env_path):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "freeze", "--local", ">", "requirements.txt"], shell=True, check=True, text=True)

def upgrade_packages(env_path):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)

def list_installed_packages(env_path):
    result = subprocess.run([os.path.join(env_path, "bin", "pip"), "list"], capture_output=True, check=True, text=True)
    print("\nInstalled packages in the selected environment:")
    print(result.stdout)

def create_requirements_file(env_path):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "freeze", "--local", ">", "requirements.txt"], shell=True, check=True)

def prompt_user(message, default_value):
    user_input = input(f"{message} (default: {default_value}): ").strip()
    return user_input or default_value

def yes_no_prompt(message):
    user_input = input(f"{message} (y/n): ").strip().lower()
    return user_input == 'y'


def main():
    if not is_executable_installed("python3"):
        print("Python 3 is not installed. Please install Python 3 and try again.")
        sys.exit(1)

    if not is_executable_installed("pip"):
        print("pip is not installed. Please install pip and try again.")
        sys.exit(1)

    default_folder_path = os.path.join(os.path.expanduser("~"), "python_envs")
    folder_path = prompt_user("Enter the folder path for the virtual environments", default_folder_path)

    os.makedirs(folder_path, exist_ok=True)

    existing_envs = search_existing_envs(folder_path)
    if existing_envs:
        print(f"\nFound existing virtual environments in {folder_path}:")
        for i, env in enumerate(existing_envs, start=1):
            print(f"{i}. {env}")
        print("0. Create new virtual environment")

        env_choice = int(prompt_user("Enter the number of the virtual environment to use, or 0 to create a new one", "0"))

        if 0 < env_choice <= len(existing_envs):
            env_name = existing_envs[env_choice - 1]
            env_path = os.path.join(folder_path, env_name)
            print(f"Using existing virtual environment: {env_name}")
        else:
            env_name = prompt_user("Enter the name of the new virtual environment", "my_project_env")
            env_path = os.path.join(folder_path, env_name)
            print(f"Creating virtual environment at {env_path}...")
            create_virtual_environment(env_path)
    else:
        env_name = prompt_user("Enter the name of the virtual environment", "my_project_env")
        env_path = os.path.join(folder_path, env_name)
        print(f"Creating virtual environment at {env_path}...")
        create_virtual_environment(env_path)

    activate_script = os.path.join(env_path, "bin", "activate")

    print(f"\nTo activate the virtual environment, run: source {activate_script}")

    print("\nUpgrading pip, setuptools, and wheel...")
    upgrade_packages(env_path)
    print("\nDone! You can now install packages using pip inside your virtual environment.")

    return env_path  # Add this line to the end of main()
if __name__ == "__main__":
    env_path = main()

    if yes_no_prompt("\nDo you want to see the list of installed packages in the selected environment?"):
        list_installed_packages(env_path)

    if yes_no_prompt("\nDo you want to create a requirements.txt file for the installed packages in the selected environment?"):
        create_requirements_file(env_path)
        print("requirements.txt file created successfully.")
