# import required modules
import subprocess
import logging
import json

# Configure logging to a file
logging.basicConfig(filename='installation.log', level=logging.INFO)

# Function to execute a command using subprocess
def run_command(command):
    # Execute the command and handle any errors
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {command}")
        logging.error(e.output.decode())
        raise


# Function to install LightDM and LightDM greeter
def install_lightdm():
    logging.info("Installing LightDM...")
    # Install LightDM and LightDM greeter using package manager
    run_command("sudo pacman -S lightdm lightdm-gtk-greeter")
    # Enable LightDM service to start on boot
    run_command("sudo systemctl enable lightdm")
    logging.info("LightDM installation completed.")


# Function to install BSPWM window manager and SXHKD hotkey daemon
def install_bspwm():
    logging.info("Installing bspwm...")
    # Install BSPWM and SXHKD using package manager
    run_command("sudo pacman -S bspwm sxhkd")
    logging.info("bspwm installation completed.")

# Function to configure LightDM
def configure_lightdm():
    logging.info("Configuring LightDM...")
    # Set the greeter session for LightDM
    run_command("sudo sed -i 's/^#greeter-session=.*/greeter-session=lightdm-gtk-greeter/' /etc/lightdm/lightdm.conf")
    # Set the session wrapper to start BSPWM for LightDM sessions
    run_command("echo '[Seat:*]\nsession-wrapper=/etc/lightdm/Xsession' | sudo tee -a /etc/lightdm/lightdm.conf")
    # Create the Xsession file to start BSPWM
    run_command("sudo bash -c 'echo -e \"#!/bin/bash\\nexec bspwm\" > /etc/lightdm/Xsession'")
    # Make the Xsession file executable
    run_command("sudo chmod +x /etc/lightdm/Xsession")
    logging.info("LightDM configuration completed.")


# Function to install i3 window manager and i3status
def install_i3wm():
    logging.info("Installing i3wm...")
    # Install i3-gaps and i3status using package manager
    run_command("sudo pacman -S i3-gaps i3status")
    logging.info("i3wm installation completed.")

# Function to configure i3 window manager
def configure_i3wm():
    logging.info("Configuring i3wm...")
    # Add configuration steps for i3wm here
    logging.info("i3wm configuration completed.")

# Function to install Xfce desktop environment and Xfce goodies
def install_xfce():
    logging.info("Installing Xfce...")
    # Install Xfce and Xfce goodies using package manager
    run_command("sudo pacman -S xfce4 xfce4-goodies")
    logging.info("Xfce installation completed.")

# Function to install GNOME desktop environment
def install_gnome():
    logging.info("Installing GNOME...")
    # Install GNOME using package manager
    run_command("sudo pacman -S gnome")
    logging.info("GNOME installation completed.")


# Function to install dwm window manager
def install_dwm():
    logging.info("Installing dwm...")
    # Install dwm using the package manager
    run_command("sudo pacman -S dwm")
    logging.info("dwm installation completed.")

# Function to install awesome window manager
def install_awesome():
    logging.info("Installing awesome...")
    # Install awesome using the package manager
    run_command("sudo pacman -S awesome")
    logging.info("awesome installation completed.")

# Function to install xmonad window manager
def install_xmonad():
    logging.info("Installing xmonad...")
    # Install xmonad using the package manager
    run_command("sudo pacman -S xmonad")
    logging.info("xmonad installation completed.")

# Function to install additional programs from a JSON config file
def install_additional_programs(config_file):
    logging.info("Installing additional programs...")
    # Load the list of additional programs from the JSON config file
    with open(config_file) as f:
        programs = json.load(f)
    # Install each program using the package manager
    for program in programs:
        run_command(f"sudo pacman -S {program}")
    logging.info("Additional programs installation completed.")


# Function to configure additional programs
def configure_additional_programs():
    logging.info("Configuring additional programs...")
    # Add configuration steps for additional programs here
    logging.info("Additional programs configuration completed.")

# Function to perform post-installation steps
def perform_post_installation_steps():
    logging.info("Performing post-installation steps...")
    # Add post-installation steps here
    logging.info("Post-installation steps completed.")

# Function to reboot the system
def reboot_system():
    logging.info("Rebooting the system...")
    # Reboot the system using the command
    run_command("sudo reboot")

# Function to update the system packages
def update_system():
    logging.info("Updating the system...")
    # Update system packages using the package manager
    run_command("sudo pacman -Syu")
    logging.info("System update completed.")

# Function to perform rollback steps
def rollback():
    logging.info("Performing rollback...")
    # Add rollback steps here
    logging.info("Rollback completed.")

# Function to setup logging configuration
def setup_logging():
    # Additional logging configuration, if needed
    pass

# Function to perform cleanup steps
def cleanup():
    logging.info("Cleaning up...")
    # Add cleanup steps here, if necessary
    logging.info("Cleanup completed.")


# Function to prompt the user for input with given message and options
def prompt_user(message, options):
    user_input = ""
    while user_input not in options:
        user_input = input(message)
    return user_input



# Main function


# Main function
if __name__ == "__main__":
    try:
        setup_logging()

        # Prompt the user to select the desktop manager to install
        install_desktop_manager = prompt_user("Select the desktop manager to install (xfce/gnome): ", ["xfce", "gnome"])
        if install_desktop_manager == "xfce":
            install_xfce()
        elif install_desktop_manager == "gnome":
            install_gnome()

        # Prompt the user to select the window manager to install
        install_window_manager = prompt_user("Select the window manager to install (lightdm/bspwm/i3wm/other): ", ["lightdm", "bspwm", "i3wm", "other"])
        if install_window_manager == "lightdm":
            install_lightdm()
            configure_lightdm()
        elif install_window_manager == "bspwm":
            install_bspwm()
            # Additional configuration steps for BSPWM
        elif install_window_manager == "i3wm":
            install_i3wm()
            configure_i3wm()
        elif install_window_manager == "other":
            install_other_tiling_window_manager = prompt_user("Enter the name of the tiling window manager to install (dwm/awesome/xmonad): ", ["dwm", "awesome", "xmonad"])
            if install_other_tiling_window_manager == "dwm":
                install_dwm()
                # Additional configuration steps for dwm
            elif install_other_tiling_window_manager == "awesome":
                install_awesome()
                # Additional configuration steps for awesome
            elif install_other_tiling_window_manager == "xmonad":
                install_xmonad()
                # Additional configuration steps for xmonad

        # Install additional programs from the config file
        install_additional_programs("additional_programs.json")

        # Configure additional programs
        configure_additional_programs()

        # Perform post-installation steps
        perform_post_installation_steps()

        # Reboot the system
        reboot_system()

    except Exception as e:
        logging.error(f"Error during script execution: {str(e)}")
        print("An error occurred during the installation process. Please check the log file for details.")
        # Perform rollback if needed
        rollback()
        raise

    finally:
        # Clean up any resources or temporary files
        cleanup()
