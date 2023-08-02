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
accountservice_file = accountservice_dir / os.getlogin() # get current username

# Create config directories
bspwm_dir.mkdir(parents=True, exist_ok=True)
sxhkd_dir.mkdir(parents=True, exist_ok=True)
polybar_dir.mkdir(parents=True, exist_ok=True)
lightdm_config_dir.mkdir(parents=True, exist_ok=True)
accountservice_dir.mkdir(parents=True, exist_ok=True)

def install():
    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'bspwm'], check=True)
    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'sxhkd'], check=True)
    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'polybar'], check=True)
    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'lightdm'], check=True)
    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'lightdm-gtk-greeter'], check=True)

def setup_config_files():
    # Sample config file contents, replace with your actual contents
    bspwm_config = """
    # BSPWM config content
    """
    sxhkd_config = """
    # SXHKD config content
    """
    polybar_config = """
    # Polybar config content
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
    # Add the execution command of bspwm to the .xinitrc file
    with open(bspwm_autostart_file, 'a') as file:
        file.write("\nexec bspwm\n")

    # Create a .desktop file for bspwm
    desktop_file_content = """
    [Desktop Entry]
    Type=Application
    Exec=bspwm
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    Name[en_US]=bspwm
    Name=bspwm
    Comment[en_US]=
    Comment=
    """
    bspwm_desktop_file.parent.mkdir(parents=True, exist_ok=True)

    with open(bspwm_desktop_file, 'w') as file:
        file.write(desktop_file_content)

    # Enable LightDM
    subprocess.run(['sudo', 'systemctl', 'enable', 'lightdm.service'], check=True)

# Call the function to install the software and set up the config files
install()
setup_config_files()
enable_at_start()
