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
    package_manager = "pacman" if os.path.exists("/usr/bin/pacman") else "yay"
    subprocess.run([f"sudo {package_manager} -Syu --noconfirm"])
    subprocess.run([f"sudo {package_manager} -S --noconfirm"] + packages)


def tips_and_tricks():
    print_colored("TIPS AND TRICKS\n", "1;33")

    # Tip 1: Changing colorscheme
    print("1. To change the colorscheme of Alacritty, you can use a color scheme from the alacritty-theme repository.")
    print("   The available colorschemes can be found in the alacritty-theme repository at https://github.com/alacritty/alacritty-theme.")
    print("   To install a colorscheme, download the .yml file for the colorscheme you want, and place it in the ~/.config/alacritty/ directory.")
    print("   Then, update the 'colors' section of the Alacritty configuration file to use the new colorscheme.")
    print("   For example, to use the 'Solarized Dark' colorscheme, add the following to your Alacritty configuration file:")
    print("   colors: solarized_dark\n")

    # Tip 2: Using mouse in Alacritty
    print("2. You can use the mouse in Alacritty to select text and URLs, and to scroll through the terminal output.")
    print("   To select text, simply click and drag to highlight the text you want to select.")
    print("   To select a URL, hold down the 'Ctrl' key and click on the URL.")
    print("   To scroll through the terminal output, use the scroll wheel on your mouse or hold down the 'Shift' key and scroll.")
    print("   To copy selected text to the clipboard, use 'Ctrl+Shift+C'.")
    print("   To paste text from the clipboard, use 'Ctrl+Shift+V'.\n")

    # Tip 3: Using ZSH with Alacritty
    print("3. You can boost your productivity with ZSH and Alacritty by using ZSH's advanced features.")
    print("   To use ZSH with Alacritty, set the 'shell.program' option in your Alacritty configuration file to '/bin/zsh'.")
    print("   To install ZSH, run 'sudo pacman -S zsh' or 'yay -S zsh' depending on your package manager.")
    print("   To install the powerlevel10k prompt for ZSH, run 'git clone https://github.com/romkatv/powerlevel10k.git ~/.oh-my-zsh/custom/themes/powerlevel10k' and add the line 'ZSH_THEME=\"powerlevel10k/powerlevel10k\"' to your ~/.zshrc file.")
    print("   Then, run 'source ~/.zshrc' to reload your ZSH configuration.")
    print("   You can further customize your ZSH prompt by running 'p10k configure'.\n")



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
tips_and_tricks()
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
    package_manager = "pacman" if os.path.exists("/usr/bin/pacman") else "yay"
    subprocess.run([f"sudo {package_manager} -Syu --noconfirm"])
    subprocess.run([f"sudo {package_manager} -S --noconfirm"] + packages)


def tips_and_tricks():
    print_colored("TIPS AND TRICKS\n", "1;33")

    # Tip 1: Changing colorscheme
    print("1. To change the colorscheme of Alacritty, you can use a color scheme from the alacritty-theme repository.")
    print("   The available colorschemes can be found in the alacritty-theme repository at https://github.com/alacritty/alacritty-theme.")
    print("   To install a colorscheme, download the .yml file for the colorscheme you want, and place it in the ~/.config/alacritty/ directory.")
    print("   Then, update the 'colors' section of the Alacritty configuration file to use the new colorscheme.")
    print("   For example, to use the 'Solarized Dark' colorscheme, add the following to your Alacritty configuration file:")
    print("   colors: solarized_dark\n")

    # Tip 2: Using mouse in Alacritty
    print("2. You can use the mouse in Alacritty to select text and URLs, and to scroll through the terminal output.")
    print("   To select text, simply click and drag to highlight the text you want to select.")
    print("   To select a URL, hold down the 'Ctrl' key and click on the URL.")
    print("   To scroll through the terminal output, use the scroll wheel on your mouse or hold down the 'Shift' key and scroll.")
    print("   To copy selected text to the clipboard, use 'Ctrl+Shift+C'.")
    print("   To paste text from the clipboard, use 'Ctrl+Shift+V'.\n")

    # Tip 3: Using ZSH with Alacritty
    print("3. You can boost your productivity with ZSH and Alacritty by using ZSH's advanced features.")
    print("   To use ZSH with Alacritty, set the 'shell.program' option in your Alacritty configuration file to '/bin/zsh'.")
    print("   To install ZSH, run 'sudo pacman -S zsh' or 'yay -S zsh' depending on your package manager.")
    print("   To install the powerlevel10k prompt for ZSH, run 'git clone https://github.com/romkatv/powerlevel10k.git ~/.oh-my-zsh/custom/themes/powerlevel10k' and add the line 'ZSH_THEME=\"powerlevel10k/powerlevel10k\"' to your ~/.zshrc file.")
    print("   Then, run 'source ~/.zshrc' to reload your ZSH configuration.")
    print("   You can further customize your ZSH prompt by running 'p10k configure'.\n")



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
tips_and_tricks()
