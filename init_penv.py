#!/usr/bin/env python3


import os
import shutil
import subprocess
import sys
import platform
import logging
from console import Console
from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)



def delete_virtual_environment(env_path):
    shutil.rmtree(env_path)
    logging.info(f"Deleted virtual environment at {env_path}")
    print(f"Deleted virtual environment at {env_path}")


def clone_virtual_environment(src_env_path, dest_env_name, folder_path):
    dest_env_path = os.path.join(folder_path, dest_env_name)
    shutil.copytree(src_env_path, dest_env_path)
    logging.info(f"Cloned virtual environment at {dest_env_path}")
    print(f"Cloned virtual environment at {dest_env_path}")


def update_package(env_path, package_name):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "install", "--upgrade", package_name], check=True)
    logging.info(f"{package_name} updated successfully.")
    print(f"{package_name} updated successfully.")


def downgrade_package(env_path, package_name, version):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "install", f"{package_name}=={version}"], check=True)
    logging.info(f"{package_name} downgraded to version {version}.")
    print(f"{package_name} downgraded to version {version}.")


def uninstall_package(env_path, package_name):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "uninstall", "-y", package_name], check=True)
    logging.info(f"{package_name} uninstalled successfully.")
    print(f"{package_name} uninstalled successfully.")


def is_executable_installed(executable):
    try:
        subprocess.run([executable, "--version"], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        return False


def search_existing_envs(folder_path):
    envs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    return envs


def create_virtual_environment(env_path):
    python_executable = "python3" if platform.system() != "Windows" else "python"
    subprocess.run([python_executable, "-m", "venv", env_path], check=True)
    logging.info(f"Created virtual environment at {env_path}")
    print(f"Created virtual environment at {env_path}")


def create_requirements_file(env_path):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "freeze", "--local", ">", "requirements.txt"], shell=True, check=True, text=True)
    logging.info("requirements.txt file created successfully.")
    print("requirements.txt file created successfully.")


def upgrade_packages(env_path):
    subprocess.run([os.path.join(env_path, "bin", "pip"), "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    logging.info("pip, setuptools, and wheel upgraded successfully.")
    print("pip, setuptools, and wheel upgraded successfully.")

def list_installed_packages(env_path):
    result = subprocess.run([os.path.join(env_path, "bin", "pip"), "list"], capture_output=True, check=True, text=True)

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Package")
    table.add_column("Version")

    lines = result.stdout.split("\n")[2:-1]  # Remove header lines and trailing newline
    for line in lines:
        package, version = line.split()
        table.add_row(package, version)

    console.print("\nInstalled packages in the selected environment:")
    console.print(table)

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

    if platform.system() == 'Windows':
        activate_script = os.path.join(env_path, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(env_path, "bin", "activate")

    print(f"\nTo activate the virtual environment, run: {activate_script}")

    print("\nUpgrading pip, setuptools, and wheel...")
    upgrade_packages(env_path)
    print("\nDone! You can now install packages using pip inside your virtual environment.")

    return env_path


def search_and_install_packages(env_path):
    try:
        subprocess.run([os.path.join(env_path, "bin", "pip"), "install", "pip_search"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to install pip_search. Skipping package search and installation.")
        return

    while True:
        search_term = input("Enter the package name to search or 'q' to quit: ").strip()
        if search_term.lower() == 'q':
            break

        search_command = f"{os.path.join(env_path, 'bin', 'python')} -m pip_search {search_term}"
        result = subprocess.run(search_command, capture_output=True, check=True, text=True, shell=True)
        print(f"\nSearch results for '{search_term}':\n{result.stdout}")

        package_to_install = input("Enter the package name to install or 'q' to quit: ").strip()
        if package_to_install.lower() == 'q':
            break
        subprocess.run([os.path.join(env_path, "bin", "pip"), "install", package_to_install], check=True)
        print(f"\n{package_to_install} installed successfully.")


# Modify main_loop function
def main_loop(env_path):
    while True:
        action = prompt_for_action()

        if action == '1':
            list_installed_packages(env_path)
        elif action == '2':
            create_requirements_file(env_path)
            print("requirements.txt file created successfully.")
        elif action == '3':
            search_and_install_packages(env_path)
        elif action == '4':
            delete_virtual_environment(env_path)
            break
        elif action == '5':
            dest_env_name = prompt_user("Enter the name of the cloned virtual environment", "cloned_env")
            clone_virtual_environment(env_path, dest_env_name, os.path.dirname(env_path))
        elif action == '6':
            package_name = input("Enter the package name to update: ").strip()
            update_package(env_path, package_name)
        elif action == '7':
            package_name = input("Enter the package name to downgrade: ").strip()
            version = input("Enter the version to downgrade to: ").strip()
            downgrade_package(env_path, package_name, version)
        elif action == '8':
            package_name = input("Enter the package name to uninstall: ").strip()
            uninstall_package(env_path, package_name)
        elif action.lower() == 'q':
            break
        else:
            print("Invalid input. Please try again.")

# Modify prompt_for_action function
def prompt_for_action():
    console = Console()
    console.print("\nChoose an action:", style="bold")
    console.print("1. List installed packages")
    console.print("2. Create requirements.txt file")
    console.print("3. Search and install pip packages")
    console.print("4. Delete virtual environment")
    console.print("5. Clone virtual environment")
    console.print("6. Update a package")
    console.print("7. Downgrade a package")
    console.print("8. Uninstall a package")
    console.print("q. Quit")

    user_input = input("Enter the number of the action or 'q' to quit: ").strip()
    return user_input

if __name__ == "__main__":
    env_path = main()
    main_loop(env_path)
