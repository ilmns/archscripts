import os
import shutil
import subprocess

# Function to print colored messages
def print_colored(msg, color_code):
    print(f"\033[{color_code}m{msg}\033[0m")

# Function to run a command and handle success/failure outputs
def run_command(command, success_msg, fail_msg, color_code):
    result = subprocess.run(command)
    if result.returncode == 0:
        print_colored(success_msg, color_code)
    else:
        print_colored(fail_msg, "1;31")
        exit(1)

# Function to install a package from official repositories
def install_package(package):
    run_command(["sudo", "pacman", "-S", "--noconfirm", package],
                f"{package} installed successfully!",
                f"Failed to install {package}.",
                "1;32")

# Function to install a package from AUR
def install_aur_package(package):
    run_command(["yay", "-S", "--noconfirm", package],
                f"{package} installed successfully!",
                f"Failed to install {package}.",
                "1;32")

# Function to backup a file
def backup_file(file):
    if os.path.isfile(file):
        backup = f"{file}.bak"
        print_colored(f"Backing up {file} to {backup}...", "1;34")
        shutil.copy(file, backup)

# Function to update system packages
def update_packages():
    print_colored("Updating system packages...", "1;34")
    run_command(["sudo", "pacman", "-Syu", "--noconfirm"],
                "System packages updated successfully!",
                "Failed to update system packages.",
                "1;32")

# Function to update AUR packages
def update_aur_packages():
    print_colored("Updating AUR packages...", "1;34")
    run_command(["yay", "-Syu", "--noconfirm"],
                "AUR packages updated successfully!",
                "Failed to update AUR packages.",
                "1;32")

# Function to install necessary packages
def install_packages(packages):
    for package in packages:
        install_package(package)

# Function to install yay if it isn't installed
def install_yay():
    if shutil.which('yay') is None:
        print_colored("Installing Yay...", "1;34")
        if subprocess.run(["git", "clone", "https://aur.archlinux.org/yay.git"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            os.chdir("yay")
            run_command(["makepkg", "-si", "--noconfirm"], "Yay installed successfully!", "Failed to install Yay.", "1;32")
            os.chdir("..")
            shutil.rmtree("yay")
        else:
            print_colored("Failed to clone Yay from git. Please check your internet connection.", "1;31")
            exit(1)

# Function to create necessary directories
def create_directories(directories):
    for directory in directories:
        os.makedirs(os.path.expanduser(directory), exist_ok=True)

# Function to write config files
def write_config_file(file, content, mode=0o755):
    with open(os.path.expanduser(file), "w") as f:
        f.write(content)
    os.chmod(os.path.expanduser(file), mode)

# Function to update .xinitrc with startup commands
def update_xinitrc(commands):
    with open(os.path.expanduser("~/.xinitrc"), "a") as f:
        for command in commands:
            f.write(f"exec {command}\n")

# Function to select bspwm as the default window manager
def select_bspwm():
    lightdm_conf_file = "/etc/lightdm/lightdm.conf"
    lightdm_conf_backup = "/etc/lightdm/lightdm.conf.bak"
    lightdm_conf_modified = "/etc/lightdm/lightdm.conf.modified"

    # Backup original lightdm.conf if not already backed up
    if not os.path.isfile(lightdm_conf_backup):
        shutil.copy(lightdm_conf_file, lightdm_conf_backup)

    # Modify lightdm.conf to use bspwm as the default window manager
    with open(lightdm_conf_file, "r") as original_file, open(lightdm_conf_modified, "w") as modified_file:
        for line in original_file:
            if line.strip().startswith("exec"):
                modified_file.write("exec bspwm\n")
            else:
                modified_file.write(line)

    # Replace original lightdm.conf with the modified version
    shutil.move(lightdm_conf_modified, lightdm_conf_file)

    print_colored("bspwm selected as the default window manager.", "1;32")

def main():
    # Update system and AUR packages
    update_packages()
    update_aur_packages()

    # Install necessary packages
    packages = ["xorg-server", "bspwm", "sxhkd", "polybar", "picom", "feh", "rofi", "dunst"]
    install_packages(packages)

    # Install yay
    install_yay()

    # Install polybar-bspwm from AUR
    install_aur_package("polybar-bspwm")

    # Create necessary directories
    directories = ["~/.config/bspwm", "~/.config/sxhkd"]
    create_directories(directories)

    # Backup existing config files
    backup_file("~/.config/bspwm/bspwmrc")
    backup_file("~/.config/sxhkd/sxhkdrc")

    bspwmrc_content = """#!/bin/bash
    sxhkd &
    polybar bspwm &
    dunst &
    exec bspwm
    """

    sxhkdrc_content = """super + Return
        alacritty
    super + Shift + q
        bspc window -c
    super + {h,j,k,l}
        bspc node -{f,s} {left,down,up,right}
    super + {Left,Down,Up,Right}
        bspc node -{f,s} {west,south,north,east}
    """

    # Write config files
    write_config_file("~/.config/bspwm/bspwmrc", bspwmrc_content)
    write_config_file("~/.config/sxhkd/sxhkdrc", sxhkdrc_content)

    # Backup .xinitrc
    backup_file("~/.xinitrc")

    # Update .xinitrc with startup commands
    startup_commands = ["bspwm", "sxhkd", "dunst"]
    update_xinitrc(startup_commands)

    # Select bspwm as the default window manager
    select_bspwm()

    # Start X server with bspwm, sxhkd, and dunst
    print_colored("Starting X server with bspwm, sxhkd, and dunst...", "1;34")
    subprocess.run(["startx"])

# Execute the main function
if __name__ == "__main__":
    main()

# Print upgraded program
with open(__file__, "r") as f:
    upgraded_program = f.read()
print("\nUpgraded Program:\n")
print(upgraded_program)
