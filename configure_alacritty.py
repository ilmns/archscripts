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

def configure_alacritty():
    alacritty_config_dir = os.path.expanduser("~/.config/alacritty")
    alacritty_config_file = os.path.join(alacritty_config_dir, "alacritty.yml")

    # Backup existing Alacritty config
    backup_file(alacritty_config_file)

    # Create Alacritty configuration directory if it doesn't exist
    create_config_directory(alacritty_config_dir)

    alacritty_config_content = '''
# Alacritty Configuration for Maximum Performance and Copy-Paste Support

# Use dynamic padding to maximize terminal window size
window:
  dynamic_padding: true

# Set scrolling history to a lower value to reduce memory usage
scrolling:
  history: 1000

# Use the fastest available OpenGL version
render_timer: true
persistent_logging: false

key_bindings:
  # Copy
  - { key: C,        mods: Control, action: Copy             }
  # Paste
  - { key: V,        mods: Control, action: Paste            }
'''

    # Write Alacritty configuration
    write_config(alacritty_config_file, alacritty_config_content)

    print_colored("Alacritty configuration updated for maximum performance and copy-paste support.", "1;32")

configure_alacritty()
