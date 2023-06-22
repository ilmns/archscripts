import subprocess
import logging
import json
import argparse

logging.basicConfig(filename='installation.log', level=logging.INFO)


def run_command(command, dry_run=False):
    if dry_run:
        logging.info(f"[Dry Run] Skipping command execution: {command}")
    else:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command: {command}")
            logging.error(e.output.decode())
            raise


def install_package(package_name, dry_run=False):
    logging.info(f"Installing {package_name}...")
    run_command(f"sudo pacman -S {package_name}", dry_run)
    logging.info(f"{package_name} installation completed.")


def prompt_user(message, options):
    user_input = ""
    while user_input not in options:
        user_input = input(message)
    return user_input


def enable_service(service_name):
    run_command(f"sudo systemctl enable {service_name}")


def configure_lightdm():
    logging.info("Configuring LightDM...")
    run_command("sudo sed -i 's/^#greeter-session=.*/greeter-session=lightdm-gtk-greeter/' /etc/lightdm/lightdm.conf")
    run_command("echo '[Seat:*]\nsession-wrapper=/etc/lightdm/Xsession' | sudo tee -a /etc/lightdm/lightdm.conf")
    run_command("sudo bash -c 'echo -e \"#!/bin/bash\\nexec bspwm\" > /etc/lightdm/Xsession'")
    run_command("sudo chmod +x /etc/lightdm/Xsession")
    logging.info("LightDM configuration completed.")


def configure_i3wm():
    logging.info("Configuring i3wm...")
    # Add configuration steps for i3wm here
    logging.info("i3wm configuration completed.")


def install_desktop_manager(dry_run=False):
    options = ["xfce", "gnome", "kde", "mate"]
    desktop_manager = prompt_user(f"Select the desktop manager to install ({'/'.join(options)}): ", options)
    install_package(desktop_manager, dry_run)
    if desktop_manager == "gnome":
        logging.info("Configuring GNOME...")
        # Additional configuration steps for GNOME
        logging.info("GNOME configuration completed.")
    elif desktop_manager == "xfce":
        logging.info("Configuring Xfce...")
        # Additional configuration steps for Xfce
        logging.info("Xfce configuration completed.")
    elif desktop_manager == "kde":
        logging.info("Configuring KDE...")
        # Additional configuration steps for KDE
        logging.info("KDE configuration completed.")
    elif desktop_manager == "mate":
        logging.info("Configuring MATE...")
        # Additional configuration steps for MATE
        logging.info("MATE configuration completed.")


def install_window_manager(dry_run=False):
    options = ["lightdm", "bspwm", "i3wm", "dwm", "awesome", "xmonad"]
    window_manager = prompt_user(f"Select the window manager to install ({'/'.join(options)}): ", options)
    if window_manager == "lightdm":
        install_package("lightdm", dry_run)
        install_package("lightdm-gtk-greeter", dry_run)
        configure_lightdm()
        enable_service("lightdm")
    elif window_manager == "bspwm":
        install_package("bspwm", dry_run)
        install_package("sxhkd", dry_run)
        # Additional configuration steps for BSPWM
    elif window_manager == "i3wm":
        install_package("i3-gaps", dry_run)
        install_package("i3status", dry_run)
        configure_i3wm()
    elif window_manager in ["dwm", "awesome", "xmonad"]:
        install_package(window_manager, dry_run)
        # Additional configuration steps for the other window managers


def install_stacking_window_manager(dry_run=False):
    logging.info("Installing stacking window manager...")
    # Add installation steps for stacking window manager
    logging.info("Stacking window manager installation completed.")


def install_tiling_window_manager(dry_run=False):
    logging.info("Installing tiling window manager...")
    # Add installation steps for tiling window manager
    logging.info("Tiling window manager installation completed.")


def install_dynamic_window_manager(dry_run=False):
    logging.info("Installing dynamic window manager...")
    # Add installation steps for dynamic window manager
    logging.info("Dynamic window manager installation completed.")


def install_additional_programs(config_file, dry_run=False):
    logging.info("Installing additional programs...")
    with open(config_file) as f:
        programs = json.load(f)
    for program in programs:
        install_package(program, dry_run)
    logging.info("Additional programs installation completed.")


def configure_additional_programs(dry_run=False):
    logging.info("Configuring additional programs...")
    # Add configuration steps for additional programs here
    logging.info("Additional programs configuration completed.")


def perform_post_installation_steps(dry_run=False):
    logging.info("Performing post-installation steps...")
    # Add post-installation steps here
    logging.info("Post-installation steps completed.")


def update_system():
    logging.info("Updating the system...")
    run_command("sudo pacman -Syu")
    logging.info("System update completed.")


def reboot_system():
    logging.info("Rebooting the system...")
    run_command("sudo reboot")


def rollback():
    logger = logging.getLogger(__name__)
    logger.info("Performing rollback...")

    try:
        # Step 1: Revert changes in the database
        logger.info("Reverting changes in the database...")
        # Code to revert changes in the database goes here
        # For example: db_revert_changes()

        # Step 2: Restore backup files
        logger.info("Restoring backup files...")
        # Code to restore backup files goes here
        # For example: restore_backup_files()

        # Step 3: Undo any file modifications
        logger.info("Undoing file modifications...")
        # Code to undo file modifications goes here
        # For example: undo_file_modifications()

        logger.info("Rollback steps completed successfully.")
    except Exception as e:
        logger.exception("Error occurred during rollback: %s", str(e))
        # You can handle the error here, such as raising an exception or taking appropriate actions based on your application's needs.
        # You may also log more details about the error if necessary.

    logger.info("Rollback completed.")


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def cleanup():
    logging.info("Cleaning up...")
    # Add cleanup steps here, if necessary
    logging.info("Cleanup completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Installation script")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without executing commands")
    args = parser.parse_args()

    try:
        setup_logging()

        install_desktop_manager(dry_run=args.dry_run)
        install_window_manager(dry_run=args.dry_run)
        install_stacking_window_manager(dry_run=args.dry_run)
        install_tiling_window_manager(dry_run=args.dry_run)
        install_dynamic_window_manager(dry_run=args.dry_run)

        install_additional_programs("additional_programs.json", dry_run=args.dry_run)
        configure_additional_programs(dry_run=args.dry_run)

        perform_post_installation_steps(dry_run=args.dry_run)
        update_system()
        reboot_system()

    except Exception as e:
        logging.error(f"Error during script execution: {str(e)}")
        print("An error occurred during the installation process. Please check the log file for details.")
        rollback()
        raise

    finally:
        cleanup()
