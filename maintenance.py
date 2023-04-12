#!/usr/bin/python
import os
import subprocess
import shutil
from termcolor import colored
from prettytable import PrettyTable
from datetime import datetime


if os.geteuid() != 0:
    print(colored("You need to have root privileges to run this script.", "red"))
    exit(1)

# Check for outdated packages
outdated_packages = subprocess.run(["pacman", "-Qu"], capture_output=True, text=True)
if outdated_packages.returncode == 0:
    print(colored("Outdated packages found:", "yellow"))
    print(outdated_packages.stdout)
else:
    print("No outdated packages found.")

# Install packages
if input("Install packages? (y/n): ").lower() == "y":
    packages = input("Enter packages to install (default: pacman-mirrorlist): ")
    packages = packages.strip() if packages.strip() != "" else "pacman-mirrorlist"
    subprocess.run(["pacman", "-S", "--noconfirm", packages])

# System check
if input("Perform system check? (y/n): ").lower() == "y":
    # Check system logs
    system_logs = subprocess.run(["journalctl", "-p", "err"], capture_output=True, text=True)
    if system_logs.returncode == 0:
        print(colored("System logs:", "yellow"))
        print(system_logs.stdout)
    else:
        print("No system logs found.")

    # Check for broken symbolic links
    broken_links = [path for path, _, _ in os.walk(os.path.expanduser("~")) if os.path.islink(path) and not os.path.exists(path)]
    if broken_links:
        print(colored("Broken symbolic links found:", "yellow"))
        for path in broken_links:
            print(path)
        if input("Remove broken symbolic links? (y/n): ").lower() == "y":
            for path in broken_links:
                os.remove(path)
            print("Broken symbolic links removed.")
    else:
        print("No broken symbolic links found.")

    # Get system information
    uname = subprocess.run(["uname", "-sr"], capture_output=True, text=True).stdout.strip()
    cpu_info = subprocess.run(["lscpu"], capture_output=True, text=True).stdout.strip()
    mem_info = subprocess.run(["free", "-h"], capture_output=True, text=True).stdout.strip()
    disk_info = subprocess.run(["df", "-h"], capture_output=True, text=True).stdout.strip()

    # Print system information
    print(colored("System information:\n", "yellow"))
    print(colored(f" {uname}", "cyan"))
    print(colored(f" {cpu_info}", "cyan"))
    print(colored(f" {mem_info}", "cyan"))
    print(colored(f" {disk_info}", "cyan"))

# System optimization
if input("Perform system optimization? (y/n): ").lower() == "y":
    print(colored("The following actions will be performed:", "cyan"))
    print(colored("- Remove /tmp and /var/log directories", "yellow"))
    print(colored("- Add recommended environment variables to .bashrc", "yellow"))
    print(colored("- Update mirrorlist and package cache", "yellow"))

    if input("Are you sure you want to proceed? (y/n): ").lower() == "y":
        # Remove redundant or old files
        shutil.rmtree("/tmp", ignore_errors=True)
        shutil.rmtree("/var/log", ignore_errors=True)

        # Recommended environment variables
        print(colored("Recommended environment variables:", "yellow"))
        print(colored("export PATH=$PATH:/usr/local/bin", "cyan"))
        print(colored("export PATH=$PATH:/usr/local/bin", "cyan"))
    

    # Set environment variables
    if input("Set recommended environment variables? (y/n): ").lower() == "y":
        with open(os.path.expanduser("~/.bashrc"), "a") as f:
            f.write("export PATH=$PATH:/usr/local/bin\n")
            f.write("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib\n")

    # Update mirrorlist
    if input("Update mirrorlist? (y/n): ").lower() == "y":
        mirrorlist_folder = "/etc/pacman.d/mirrorlist"
        if not os.path.exists(mirrorlist_folder):
            os.makedirs(mirrorlist_folder)

        # Ask user to select one or more countries for repository host origin of mirrors
        country_input = input("Enter country code(s) for repository host origin of mirrors (e.g. FR,GB): ")
        if country_input == "":
            country_input = "FI"  # default to Finland if no input provided
        countries = country_input.upper().split(",")
        print(colored(f"Selected country codes: {countries}", "yellow"))

        # Fetch mirrorlist from internet and pretty print available mirrors
        response = subprocess.run(["curl", "-s", f"https://archlinux.org/mirrorlist/?country={','.join(countries)}&protocol=https&use_mirror_status=on"],
                                stdout=subprocess.PIPE)
        mirrors = response.stdout.decode().split("\n")
        for mirror in mirrors:
            if mirror.startswith("Server = "):
                print(mirror)

        # Uncomment Finland mirrors
        with open("/etc/pacman.d/mirrorlist.pacnew") as mirrors:
            finland_mirrors = []
            for line in mirrors:
                if line.startswith("#Server = http://mirror1.fin.mirror.archlinux.org/"):
                    line = line.replace("#", "")
                    finland_mirrors.append(line.strip())
                elif line.startswith("Server = http://mirror1.fin.mirror.archlinux.org/"):
                    finland_mirrors.append(line.strip())
        print(colored(f"Finland mirrors: {finland_mirrors}", "yellow"))

        # Write selected mirrors to mirrorlist.new
        with open(f"{mirrorlist_folder}/mirrorlist.new", "w") as f:
            f.write("# Updated on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            for mirror in finland_mirrors:
                response = os.system("ping -c 1 " + mirror.split("=")[1].strip())
                if response == 0:
                    f.write(f"{mirror}\n")
                    break
            else:
                print(colored(f"Unable to find a working Finland mirror to update mirrorlist", "red"))
                exit(1)
