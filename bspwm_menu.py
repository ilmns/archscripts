import os
import subprocess
from pathlib import Path

# Define paths
home_dir = Path.home()
config_dir = home_dir / ".config"
bspwm_dir = config_dir / "bspwm"
sxhkd_dir = config_dir / "sxhkd"
polybar_dir = config_dir / "polybar"
accountservice_dir = Path("/var/lib/AccountsService/users")

bspwm_config_file = bspwm_dir / "bspwmrc"
sxhkd_config_file = sxhkd_dir / "sxhkdrc"
polybar_config_file = polybar_dir / "config"
bspwm_autostart_file = home_dir / ".xinitrc"
bspwm_desktop_file = config_dir / "autostart" / "bspwm.desktop"
accountservice_file = accountservice_dir / os.getlogin()  # get current username

# Create config directories
bspwm_dir.mkdir(parents=True, exist_ok=True)
sxhkd_dir.mkdir(parents=True, exist_ok=True)
polybar_dir.mkdir(parents=True, exist_ok=True)
accountservice_dir.mkdir(parents=True, exist_ok=True)


def ask_sudo_password():
    sudo_password = input("Please enter your sudo password: ")
    return sudo_password


def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}")
        print(e)


def install_packages(sudo_password):
    packages = ["bspwm", "sxhkd", "polybar", "lightdm", "lightdm-gtk-greeter"]
    command = f"echo {sudo_password} | sudo -S pacman -S --noconfirm {' '.join(packages)}"
    run_command(command)


def setup_config_files():
    # Sample config file contents, replace with your actual contents
    bspwm_config = """
    #!/bin/bash

    # Create panels on each monitor
    for m in $(bspc query -M --names); do
        bspc monitor "$m" -d 1 2 3 4 5 || {
            echo "Failed to create panels on monitor $m"
            exit 1
        }
    done

    # Continue the rest of the bspwm config contents
    """
    sxhkd_config = """
    # Launch Thunar (File Manager)
    super + t
        thunar

    # Launch Chromium
    super + p
        chromium

    # Launch Terminator (Terminal Emulator)
    super + Return
        terminator
    """
    # Polybar config content
    polybar_config = """
    [colors]
    background = #1a1b26
    foreground = #a9b1d6
    primary = #7aa2f7
    secondary = #9ece6a
    alert = #f7768e

    ; Rest of the polybar config
    """

    accountservice_config = """
    [User]
    Language=fi_FI.UTF-8
    """

    # Write config files
    try:
        with open(bspwm_config_file, 'w') as file:
            file.write(bspwm_config)
    except Exception as e:
        print(f"Error writing bspwm config: {e}")

    try:
        with open(sxhkd_config_file, 'w') as file:
            file.write(sxhkd_config)
    except Exception as e:
        print(f"Error writing sxhkd config: {e}")

    try:
        with open(polybar_config_file, 'w') as file:
            file.write(polybar_config)
    except Exception as e:
        print(f"Error writing polybar config: {e}")

    try:
        with open(accountservice_file, 'w') as file:
            file.write(accountservice_config)
    except Exception as e:
        print(f"Error writing accountservice config: {e}")


def enable_at_start():
    with open(bspwm_autostart_file, 'a') as file:
        file.write("\nexec bspwm\n")

    desktop_file_content = """
    [Desktop Entry]
    Type=Application
    Exec=bspwm
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    Name[fi_FI]=bspwm
    Name=bspwm
    Comment[fi_FI]=
    Comment=
    """
    bspwm_desktop_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(bspwm_desktop_file, 'w') as file:
            file.write(desktop_file_content)
    except Exception as e:
        print(f"Error writing bspwm.desktop file: {e}")


def main():
    sudo_password = ask_sudo_password()
    install_packages(sudo_password)
    setup_config_files()
    enable_at_start()


if __name__ == "__main__":
    main()
