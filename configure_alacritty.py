import os
import subprocess

def print_colored(msg, color_code):
    print(f"\033[{color_code}m{msg}\033[0m")

def backup_file(file):
    if os.path.isfile(file):
        backup = f"{file}.bak"
        print_colored(f"Backing up {file} to {backup}...", "1;34")
        subprocess.run(["cp", file, backup])

def create_config_directory(directory):
    os.makedirs(directory, exist_ok=True)

def write_config(file, content):
    with open(file, "w") as f:
        f.write(content)

def install_packages(packages):
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "-y"] + packages)

def configure_alacritty(install_optional=False):
    alacritty_config_dir = os.path.expanduser("~/.config/alacritty")
    alacritty_config_file = os.path.join(alacritty_config_dir, "alacritty.yml")

    backup_file(alacritty_config_file)

    create_config_directory(alacritty_config_dir)

    alacritty_config_content = '''
window:
  dynamic_padding: true

scrolling:
  history: 1000

render_timer: true
persistent_logging: false

mouse:
  wheel:
    up:
      modifiers: []
      amount: 3
    down:
      modifiers: []
      amount: 3
  url:
    launcher: none
  selection:
    save_to_clipboard: true

history:
  search:
    reverse_search:
      key: R
      mods: Control
    forward_search:
      key: F
      mods: Control+Shift

shell:
  program: /usr/bin/zsh

'''

    if install_optional:
        install_packages(["zsh", "fonts-powerline"])
        subprocess.run(["p10k", "configure"])

    write_config(alacritty_config_file, alacritty_config_content)

    print_colored("Alacritty configuration updated for maximum performance and copy-paste support.", "1;32")


configure_alacritty()
