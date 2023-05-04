import os
import subprocess

def print_colored(msg, color_code):
    print(f"\033[{color_code}m{msg}\033[0m")

def run_command(command, success_msg, fail_msg, color_code):
    if subprocess.run(command).returncode == 0:
        print_colored(success_msg, color_code)
    else:
        print_colored(fail_msg, "1;31")
        exit(1)

def install_package(package):
    run_command(["sudo", "pacman", "-S", "--noconfirm", package],
                f"{package} installed successfully!",
                f"Failed to install {package}.",
                "1;32")

def install_aur_package(package):
    run_command(["yay", "-S", "--noconfirm", package],
                f"{package} installed successfully!",
                f"Failed to install {package}.",
                "1;32")

def backup_file(file):
    if os.path.isfile(file):
        backup = f"{file}.bak"
        print_colored(f"Backing up {file} to {backup}...", "1;34")
        subprocess.run(["cp", file, backup])

print_colored("Updating system...", "1;34")
subprocess.run(["sudo", "pacman", "-Syyu", "--noconfirm"])

packages = ["xorg-server", "bspwm", "sxhkd", "polybar", "picom", "feh", "rofi"]
for package in packages:
    install_package(package)

if subprocess.run(["command", "-v", "yay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
    print_colored("Installing Yay...", "1;34")
    run_command(["git", "clone", "https://aur.archlinux.org/yay.git"], "", "", "")
    os.chdir("yay")
    run_command(["makepkg", "-si", "--noconfirm"], "Yay installed successfully!", "Failed to install Yay.", "1;32")
    os.chdir("..")
    subprocess.run(["rm", "-rf", "yay"])

install_aur_package("polybar-bspwm")

os.makedirs(os.path.expanduser("~/.config/bspwm"), exist_ok=True)
os.makedirs(os.path.expanduser("~/.config/sxhkd"), exist_ok=True)

backup_file(os.path.expanduser("~/.config/bspwm/bspwmrc"))
backup_file(os.path.expanduser("~/.config/sxhkd/sxhkdrc"))

bspwmrc_content = """#!/bin/bash
sxhkd &
polybar bspwm &
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

with open(os.path.expanduser("~/.config/bspwm/bspwmrc"), "w") as f:
    f.write(bspwmrc_content)
subprocess.run(["chmod", "+x", os.path.expanduser("~/.config/bspwm/bspwmrc")])

with open(os.path.expanduser("~/.config/sxhkd/sxhkdrc"), "w") as f:
    f.write(sxhkdrc_content)

backup_file(os.path.expanduser("~/.xinitrc"))

with open(os.path.expanduser("~/.xinitrc"), "a") as f:
    f.write("\nexec bspwm\n")
    f.write("exec sxhkd\n")

print_colored("Starting X server with bspwm and sxhkd...", "1;34")
subprocess.run(["startx"])
