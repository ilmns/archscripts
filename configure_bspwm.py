import os
import subprocess
import shutil

CONFIG_DIR = os.path.expanduser("~/.config")

def print_colored(msg, color_code):
    print(f"\033[{color_code}m{msg}\033[0m")

def run_command(command, capture_output=False):
    if capture_output:
        return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        return subprocess.run(command)

def check_dependency(dependency):
    result = shutil.which(dependency)
    if result is None:
        print_colored(f"{dependency} is missing. Installing it...", "1;33")
        return False
    return True

def install_package(package):
    run_command(["sudo", "pacman", "-S", "--noconfirm", package])

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def handle_file(file_path, content):
    if os.path.isfile(file_path):
        print_colored(f"{file_path} already exists. Skipping...", "1;33")
    else:
        with open(file_path, "w") as f:
            f.write(content)
        print_colored(f"{file_path} created.", "1;32")

def main():
    dependencies = ["xorg-server", "bspwm", "sxhkd", "polybar", "picom", "feh", "rofi", "alacritty"]

    for dependency in dependencies:
        if not check_dependency(dependency):
            install_package(dependency)

    create_dir(os.path.join(CONFIG_DIR, "bspwm"))
    create_dir(os.path.join(CONFIG_DIR, "sxhkd"))
    create_dir(os.path.join(CONFIG_DIR, "rofi"))

    bspwmrc_content = """#!/bin/bash
sxhkd &
polybar bspwm &
picom &
feh --bg-scale /usr/share/backgrounds/default_wallpaper.jpg
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
super + d
    rofi -show drun
"""

    rofi_config_content = """rofi.theme: Arc-Dark
"""

    handle_file(os.path.join(CONFIG_DIR, "bspwm/bspwmrc"), bspwmrc_content)
    handle_file(os.path.join(CONFIG_DIR, "sxhkd/sxhkdrc"), sxhkdrc_content)
    handle_file(os.path.join(CONFIG_DIR, "rofi/config.rasi"), rofi_config_content)

    xinitrc_path = os.path.expanduser("~/.xinitrc")
    xinitrc_content = """#!/bin/sh
exec bspwm
"""

    if os.path.isfile(xinitrc_path):
        print_colored("~/.xinitrc already exists. Skipping...", "1;33")
    else:
        with open(xinitrc_path, "w") as f:
            f.write(xinitrc_content)
        os.chmod(xinitrc_path, 0o755)
        print_colored("~/.xinitrc created.", "1;32")

    print_colored("Configuration files created. Please restart the X server for the changes to take effect.", "1;32")

if __name__ == "__main__":
    main()
