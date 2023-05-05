import os
import contextlib

# Define paths
home_dir = os.path.expanduser("~")
bspwm_dir = os.path.join(home_dir, ".config", "bspwm")
sxhkd_dir = os.path.join(home_dir, ".config", "sxhkd")
polybar_dir = os.path.join(home_dir, ".config", "polybar")
bspwm_config_file = os.path.join(bspwm_dir, "bspwmrc")
sxhkd_config_file = os.path.join(sxhkd_dir, "sxhkdrc")
polybar_config_file = os.path.join(polybar_dir, "config")
bspwm_autostart_file = os.path.join(home_dir, ".xinitrc")
bspwm_desktop_file = os.path.join(home_dir, ".config", "autostart", "bspwm.desktop")

# Define menu options
options = {
    1: "Clone bspwm, sxhkd, and polybar repositories",
    2: "Install bspwm, sxhkd, and polybar",
    3: "Configure bspwm, sxhkd, and polybar",
    4: "Configure bspwm to start automatically",
    5: "View current configuration",
    6: "Exit"
}

# Define configuration options
config_options = {
    1: "Configure basic settings",
    2: "Configure advanced settings",
    3: "Back to main menu"
}

# Define git and make commands
git_clone_bspwm = "git clone https://github.com/baskerville/bspwm.git"
git_clone_sxhkd = "git clone https://github.com/baskerville/sxhkd.git"
git_clone_polybar = "git clone --recursive https://github.com/polybar/polybar.git"
make_bspwm = "make && sudo make install"
make_sxhkd = "make && sudo make install"
make_polybar = "./build.sh install"

# Create config directories
os.makedirs(bspwm_dir, exist_ok=True)
os.makedirs(sxhkd_dir, exist_ok=True)
os.makedirs(polybar_dir, exist_ok=True)

# Define functions
def clone_repos():
    with change_directory_temporarily(home_dir):
        execute_command(git_clone_bspwm, "Failed to clone bspwm repository", "Bspwm repository cloned successfully")
        execute_command(git_clone_sxhkd, "Failed to clone sxhkd repository", "Sxhkd repository cloned successfully")
        execute_command(git_clone_polybar, "Failed to clone polybar repository", "Polybar repository cloned successfully")

def install():
    with change_directory_temporarily(os.path.join(home_dir, "bspwm")):
        execute_command(make_bspwm, "Failed to compile bspwm", "Bspwm compiled successfully")
    with change_directory_temporarily(os.path.join(home_dir, "sxhkd")):
        execute_command(make_sxhkd, "Failed to compile sxhkd", "Sxhkd compiled successfully")
    with change_directory_temporarily(os.path.join(home_dir, "polybar")):
        execute_command(make_polybar, "Failed to compile polybar", "Polybar compiled successfully")

def configure():
    while True:
        os.system("clear")
        print("Choose configuration option:")
        for key in config_options:
            print(f"{key}. {config_options[key]}")
        option = input("Enter option: ")
        if option == "1":
            configure_basic()
        elif option == "2":
            configure_advanced()
        elif option == "3":
            break


def configure_basic():
    os.system(f"cp {os.path.join(bspwm_dir, 'bspwmrc.example')} {bspwm_config_file}")
    os.system(f"cp {os.path.join(sxhkd_dir, 'sxhkdrc.example')} {sxhkd_config_file}")
    os.system(f"cp {os.path.join(polybar_dir, 'config.example')} {polybar_config_file}")

def configure_advanced():
    advanced_options = {
        1: "Configure bspwm settings",
        2: "Configure sxhkd settings",
        3: "Configure polybar settings",
        4: "Back to main menu"
    }

    while True:
        os.system("clear")
        print("Choose advanced configuration option:")
        for key in advanced_options:
            print(f"{key}. {advanced_options[key]}")
        option = input("Enter option: ")
        
        if option == "1":
            configure_bspwm_advanced()
        elif option == "2":
            configure_sxhkd_advanced()
        elif option == "3":
            configure_polybar_advanced()
        elif option == "4":
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")



def configure_bspwm_advanced():
    bspwm_advanced_options = {
        1: "Change gap size",
        2: "Change border width",
        3: "Back to advanced configuration"
    }

    while True:
        os.system("clear")
        print("Choose bspwm advanced configuration option:")
        for key in bspwm_advanced_options:
            print(f"{key}. {bspwm_advanced_options[key]}")
        option = input("Enter option: ")

        if option == "1":
            change_bspwm_gap_size()
        elif option == "2":
            change_bspwm_border_width()
        elif option == "3":
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")

def change_bspwm_gap_size():
    new_gap_size = input("Enter new gap size (in pixels): ")
    try:
        gap_size_int = int(new_gap_size)
        with open(bspwm_config_file, "r") as file:
            config_lines = file.readlines()

        gap_line = next((i for i, line in enumerate(config_lines) if "bspc config window_gap" in line), None)
        if gap_line is not None:
            config_lines[gap_line] = f"bspc config window_gap {new_gap_size}\n"
        else:
            config_lines.append(f"bspc config window_gap {new_gap_size}\n")

        with open(bspwm_config_file, "w") as file:
            file.writelines(config_lines)

        print("Gap size updated successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid integer value for gap size.")

def change_bspwm_border_width():
    new_border_width = input("Enter new border width (in pixels): ")
    try:
        border_width_int = int(new_border_width)
        with open(bspwm_config_file, "r") as file:
            config_lines = file.readlines()

        border_line = next((i for i, line in enumerate(config_lines) if "bspc config border_width" in line), None)
        if border_line is not None:
            config_lines[border_line] = f"bspc config border_width {new_border_width}\n"
        else:
            config_lines.append(f"bspc config border_width {new_border_width}\n")

        with open(bspwm_config_file, "w") as file:
            file.writelines(config_lines)

        print("Border width updated successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid integer value for border width.")

def configure_sxhkd_advanced():
    sxhkd_advanced_options = {
        1: "Change key binding for an action",
        2: "Add a new key binding",
        3: "Remove a key binding",
        4: "Back to advanced configuration"
    }

    while True:
        os.system("clear")
        print("Choose sxhkd advanced configuration option:")
        for key in sxhkd_advanced_options:
            print(f"{key}. {sxhkd_advanced_options[key]}")
        option = input("Enter option: ")

        if option == "1":
            change_sxhkd_key_binding()
        elif option == "2":
            add_sxhkd_key_binding()
        elif option == "3":
            remove_sxhkd_key_binding()
        elif option == "4":
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")

def change_sxhkd_key_binding():
    action = input("Enter the action you want to change the key binding for: ")

    with open(sxhkd_config_file, "r") as file:
        config_lines = file.readlines()

    action_line = next((i for i, line in enumerate(config_lines) if action in line), None)

    if action_line is not None:
        old_key_binding = config_lines[action_line - 1].strip()
        new_key_binding = input(f"Enter the new key binding for the action (current: {old_key_binding}): ")

        config_lines[action_line - 1] = f"{new_key_binding}\n"

        with open(sxhkd_config_file, "w") as file:
            file.writelines(config_lines)

        print("Key binding updated successfully.")
    else:
        print("Action not found. Please make sure you entered the correct action.")

def add_sxhkd_key_binding():
    new_key_binding = input("Enter the new key binding: ")
    action = input("Enter the action for the new key binding: ")

    with open(sxhkd_config_file, "a") as file:
        file.write(f"\n{new_key_binding}\n{action}\n")

    print("New key binding added successfully.")

def remove_sxhkd_key_binding():
    action = input("Enter the action for the key binding you want to remove: ")

    with open(sxhkd_config_file, "r") as file:
        config_lines = file.readlines()

    action_line = next((i for i, line in enumerate(config_lines) if action in line), None)

    if action_line is not None:
        del config_lines[action_line - 1:action_line + 1]

        with open(sxhkd_config_file, "w") as file:
            file.writelines(config_lines)

        print("Key binding removed successfully.")
    else:
        print("Action not found. Please make sure you entered the correct action.")


def configure_polybar_advanced():
    polybar_advanced_options = {
        1: "Change font",
        2: "Change colors",
        3: "Configure modules",
        4: "Back to advanced configuration"
    }

    while True:
        os.system("clear")
        print("Choose polybar advanced configuration option:")
        for key in polybar_advanced_options:
            print(f"{key}. {polybar_advanced_options[key]}")
        option = input("Enter option: ")

        if option == "1":
            change_polybar_font()
        elif option == "2":
            change_polybar_colors()
        elif option == "3":
            configure_polybar_modules()
        elif option == "4":
            break
        else:
            print("Invalid choice, please try again.")
        input("Press Enter to continue...")

def change_polybar_font():
    new_font = input("Enter the new font name: ")

    with open(polybar_config_file, "r") as file:
        config_lines = file.readlines()

    font_line = next((i for i, line in enumerate(config_lines) if "font" in line and "font-" not in line), None)

    if font_line is not None:
        config_lines[font_line] = f"font = {new_font}\n"

        with open(polybar_config_file, "w") as file:
            file.writelines(config_lines)

        print("Font updated successfully.")
    else:
        print("Font configuration not found. Please make sure the polybar config file is correct.")


def change_polybar_colors():
    new_background_color = input("Enter the new background color (e.g., #1d1f21): ")
    new_foreground_color = input("Enter the new foreground color (e.g., #c5c8c6): ")
    new_accent_color = input("Enter the new accent color (e.g., #81a2be): ")

    with open(polybar_config_file, "r") as file:
        config_lines = file.readlines()

    background_line = next((i for i, line in enumerate(config_lines) if "background" in line and "background-" not in line), None)
    foreground_line = next((i for i, line in enumerate(config_lines) if "foreground" in line and "foreground-" not in line), None)
    accent_line = next((i for i, line in enumerate(config_lines) if "accent" in line and "accent-" not in line), None)

    updated = False

    if background_line is not None:
        config_lines[background_line] = f"background = {new_background_color}\n"
        updated = True

    if foreground_line is not None:
        config_lines[foreground_line] = f"foreground = {new_foreground_color}\n"
        updated = True

    if accent_line is not None:
        config_lines[accent_line] = f"accent = {new_accent_color}\n"
        updated = True

    if updated:
        with open(polybar_config_file, "w") as file:
            file.writelines(config_lines)

        print("Colors updated successfully.")
    else:
        print("Color configuration not found. Please make sure the polybar config file is correct.")


def configure_polybar_modules():
    with open(polybar_config_file, "r") as file:
        config_lines = file.readlines()

    modules_line = next((i for i, line in enumerate(config_lines) if "modules-" in line), None)

    if modules_line is not None:
        print("Current modules configuration:")
        print(config_lines[modules_line])

        new_modules = input("Enter the new modules configuration (e.g., wlan eth volume battery): ")
        config_lines[modules_line] = f"modules-center = {new_modules}\n"

        with open(polybar_config_file, "w") as file:
            file.writelines(config_lines)

        print("Modules updated successfully.")
    else:
        print("Modules configuration not found. Please make sure the polybar config file is correct.")



def check_pacman_lock():
    if os.path.exists("/var/lib/pacman/db.lck"):
        print("Pacman database is locked. If you are sure that no other package manager is running, we can remove the lock file.")
        response = input("Remove lock file? (y/n): ")
        if response.lower() == "y":
            execute_command("sudo rm /var/lib/pacman/db.lck", "Failed to remove lock file", "Lock file removed successfully")
        else:
            print("Please close any running package managers and try again.")
            return False
    return True


def configure_autostart():
    with open(bspwm_autostart_file, "w") as f:
        f.write("#!/bin/sh\n")
        f.write("sxhkd &\n")
        f.write("exec bspwm\n")
    os.system(f"chmod +x {bspwm_autostart_file}")
    with open(bspwm_desktop_file, "w") as f:
        f.write("[Desktop Entry]\n")
        f.write("Encoding=UTF-8\n")
        f.write("Name=bspwm\n")
        f.write(f"Exec={bspwm_autostart_file}\n")
        f.write("Type=Application\n")



def view_configuration():
    print("Current Configuration:")
    print("---------------------")
    # Print out the contents of the configuration files
    with open(bspwm_config_file, "r") as f:
        print(f.read())
    with open(sxhkd_config_file, "r") as f:
        print(f.read())
    # Prompt the user to press enter to continue
    input("Press Enter to continue...")



def change_directory_temporarily(path):
    @contextlib.contextmanager
    def temporary_directory_change():
        current_directory = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(current_directory)
    
    return temporary_directory_change()



def execute_command(command, error_msg, success_msg):
    exit_code = os.system(command)
    if exit_code != 0:
        print(error_msg)
    else:
        print(success_msg)


def main():
    menu_actions = {
        "1": clone_repos,
        "2": install,
        "3": configure,
        "4": configure_autostart,
        "5": view_configuration,
        "6": exit
    }

    while True:
        os.system("clear")
        print("Choose an option:")
        for key in options:
            print(f"{key}. {options[key]}")
        choice = input("Enter your choice: ")
        
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again.")
        
        if choice != "6":
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
