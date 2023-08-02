import os
import subprocess
from pathlib import Path

# Define paths
home_dir = Path.home()
config_dir = home_dir / ".config"
bspwm_dir = config_dir / "bspwm"
sxhkd_dir = config_dir / "sxhkd"
polybar_dir = config_dir / "polybar"
lightdm_config_dir = Path("/etc/lightdm")
accountservice_dir = Path("/var/lib/AccountsService/users")

bspwm_config_file = bspwm_dir / "bspwmrc"
sxhkd_config_file = sxhkd_dir / "sxhkdrc"
polybar_config_file = polybar_dir / "config"
bspwm_autostart_file = home_dir / ".xinitrc"
bspwm_desktop_file = config_dir / "autostart" / "bspwm.desktop"
lightdm_gtk_greeter_config_file = lightdm_config_dir / "lightdm-gtk-greeter.conf"
accountservice_file = accountservice_dir / os.getlogin()  # get current username

# Create config directories
bspwm_dir.mkdir(parents=True, exist_ok=True)
sxhkd_dir.mkdir(parents=True, exist_ok=True)
polybar_dir.mkdir(parents=True, exist_ok=True)
lightdm_config_dir.mkdir(parents=True, exist_ok=True)
accountservice_dir.mkdir(parents=True, exist_ok=True)


def ask_sudo_password():
    sudo_password = input("Please enter your sudo password: ")
    return sudo_password


def install_packages(sudo_password):
    try:
        packages = ["bspwm", "sxhkd", "polybar", "lightdm", "lightdm-gtk-greeter"]
        subprocess.run(['echo', sudo_password, '|', 'sudo', '-S', 'pacman', '-S', '--noconfirm'] + packages, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred during package installation:")
        print(e)
        exit(1)


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

    lightdm_gtk_greeter_config = """
    [greeter]
    theme-name = Tela
    icon-theme-name = Tela
    cursor-theme-name = Tela
    cursor-theme-size = 32
    font-name = Cantarell 20
    """

    accountservice_config = """
    [User]
    Language=fi_FI.UTF-8
    """

    # Write config files
    with open(bspwm_config_file, 'w') as file:
        file.write(bspwm_config)

    with open(sxhkd_config_file, 'w') as file:
        file.write(sxhkd_config)

    with open(polybar_config_file, 'w') as file:
        file.write(polybar_config)

    with open(lightdm_gtk_greeter_config_file, 'w') as file:
        file.write(lightdm_gtk_greeter_config)

    with open(accountservice_file, 'w') as file:
        file.write(accountservice_config)


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

    with open(bspwm_desktop_file, 'w') as file:
        file.write(desktop_file_content)

    subprocess.run(['sudo', 'systemctl', 'enable', 'lightdm.service'], check=True)


def main():
    sudo_password = ask_sudo_password()
    install_packages(sudo_password)
    setup_config_files()
    enable_at_start()


if __name__ == "__main__":
    main()
