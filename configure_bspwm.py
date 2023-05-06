#!/usr/bin/env python

import argparse, os, random, shutil, urllib.request, subprocess

CONFIG_DIR = os.path.expanduser("~/.config")

def parse_args():
    parser = argparse.ArgumentParser(description='Configure bspwm window manager.')
    parser.add_argument('--path', type=str, help='path to set wallpaper')
    parser.add_argument('--url', type=str, help='URL to download wallpaper')
    parser.add_argument('--random', action='store_true', help='set a random wallpaper')
    return parser.parse_args()

def download(url, path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
        out_file.write(response.read())

def print_color(msg, code):
    print(f"\033[{code}m{msg}\033[0m")

def exec_command(cmd, capture_output=False):
    if capture_output:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    else:
        return subprocess.run(cmd, check=True)

def package_installed(pkg):
    try:
        result = exec_command(["pacman", "-Q", pkg], capture_output=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def dep_check(dep):
    if not shutil.which(dep):
        print_color(f"{dep} is missing. Installing it...", "1;33")
        return False
    return True

def install(pkg):
    exec_command(["sudo", "pacman", "-S", "--noconfirm", pkg])

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def overwrite_prompt(path):
    response = input(f"{path} already exists. Do you want to overwrite it? (yes/no): ").lower()
    return response == "yes"

def set_wallpaper(path, url=None, args=None):
    if args and args.random:
        img_paths = [os.path.join(root, name) for root, dirs, files in os.walk("/usr/share/backgrounds") for name in files if name.endswith(".jpg")]
        if not img_paths:
            print("Error: No wallpaper files found in /usr/share/backgrounds.")
            return
        random_img = random.choice(img_paths)
        os.system(f"feh --bg-scale {random_img}")
    elif url:
        download(url, path)
        os.system(f"feh --bg-scale {path}")
    else:
        print("Error: No wallpaper specified.")
        return

def handle_file(path, content):
    if os.path.isfile(path):
        if overwrite_prompt(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print_color(f"{path} overwritten.", "1;32")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print_color(f"{path} created.", "1;32")

def choose(choices, msg):
    print(msg)
    for i, choice in enumerate(choices):
        print(f"{i+1}. {choice}")
    while True:
        try:
            choice = int(input("> "))
            if choice not in range(1, len(choices)+1):
                raise ValueError()
            break
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and", len(choices))
    return choices[choice-1]

def main():
    args = parse_args()

    dependencies = ["xorg-server", "bspwm", "sxhkd", "polybar", "picom", "feh", "rofi", "alacritty", "dmenu"]
    set_wallpaper(args.path, args.url, args)

    for dependency in dependencies:
        package = dependency
        if dependency == "alacritty":
            package = "community/alacritty"

        if not package_installed(package):
            install(package)

    make_dir(os.path.join(CONFIG_DIR, "bspwm"))
    make_dir(os.path.join(CONFIG_DIR, "sxhkd"))
    make_dir(os.path.join(CONFIG_DIR, "rofi"))
    make_dir(os.path.join(CONFIG_DIR, "picom"))

    shell_options = ["bash", "zsh", "fish"]
    default_shell = choose(shell_options, "Select default shell:")
    if default_shell == "bash":
        handle_file(os.path.expanduser("~/.bashrc"), "exec bspwm")
    elif default_shell == "zsh":
        handle_file(os.path.expanduser("~/.zshrc"), "exec bspwm")
    elif default_shell == "fish":
        handle_file(os.path.expanduser("~/.config/fish/config.fish"), "exec bspwm")


    bspwmrc_content = """#!/bin/bash
    sxhkd &
    polybar bspwm &
    picom -b &
    feh --bg-scale /usr/share/backgrounds/xfce/Butterfly.jpg
    exec bspwm
    """

    sxhkdrc_content = """super + Return
        alacritty
    super + Shift + q
        bspc window -c
    super + {h,j,k,l}
        bspc node -{focus,shift} {left,down,up,right}
    super + {Left,Down,Up,Right}
        bspc node -{focus,shift} {west,south,north,east}
    super + d
        rofi -show drun
    """

    rofi_config_content = """rofi.theme: Arc-Dark
    """

    picom_config_content = """backend = "glx";
    vsync = true;
    """

    handle_file(os.path.join(CONFIG_DIR, "bspwm/bspwmrc"), bspwmrc_content)
    handle_file(os.path.join(CONFIG_DIR, "sxhkd/sxhkdrc"), sxhkdrc_content)
    handle_file(os.path.join(CONFIG_DIR, "rofi/config.rasi"), rofi_config_content)
    handle_file(os.path.join(CONFIG_DIR, "picom/picom.conf"), picom_config_content)

    xinitrc_path = os.path.expanduser("~/.xinitrc")
    xinitrc_content = """#!/bin/sh
    exec bspwm
    """

    if os.path.isfile(xinitrc_path):
        if overwrite_prompt(xinitrc_path):
            with open(xinitrc_path, "w", encoding="utf-8") as file:
                file.write(xinitrc_content)
            os.chmod(xinitrc_path, 0o755)
            print_color("~/.xinitrc overwritten.", "1;32")
    else:
        with open(xinitrc_path, "w", encoding="utf-8") as file:
            file.write(xinitrc_content)
        os.chmod(xinitrc_path, 0o755)
        print_color("~/.xinitrc created.", "1;32")


if __name__ == "__main__":
    main()

