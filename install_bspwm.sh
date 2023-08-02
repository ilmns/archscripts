#!/usr/bin/env python3

import os
import subprocess

def run(command):
    subprocess.call(command, shell=True)

# Install packages
packages = [
    "bspwm",
    "rofi",
    "lightdm",
    "lightdm-gtk-greeter",
    "picom",
    "nitrogen",
]

for package in packages:
    run(f"sudo pacman -Syu --noconfirm --needed {package}")

# Create required directories
directories = [
    "/home/$USER/.config/bspwm",
    "/home/$USER/.config/sxhkd",
    "/home/$USER/.config/picom",
    "/home/$USER/.config/nitrogen",
]

for directory in directories:
    run(f"mkdir -p {directory}")

# Configure bspwm
run('echo "#!/bin/sh" > /home/$USER/.config/bspwm/bspwmrc')
run('echo "sxhkd &" >> /home/$USER/.config/bspwm/bspwmrc')
run('echo "picom &" >> /home/$USER/.config/bspwm/bspwmrc')
run('echo "nitrogen --restore &" >> /home/$USER/.config/bspwm/bspwmrc')
run('echo "exec bspwm" >> /home/$USER/.config/bspwm/bspwmrc')
run('chmod +x /home/$USER/.config/bspwm/bspwmrc')

# Configure sxhkd
run('touch /home/$USER/.config/sxhkd/sxhkdrc')

# Configure LightDM
run("sudo sed -i 's/^#greeter-session=.*/greeter-session=lightdm-gtk-greeter/' /etc/lightdm/lightdm.conf")
run("echo '[Seat:*]\nsession-wrapper=/etc/lightdm/Xsession' | sudo tee -a /etc/lightdm/lightdm.conf")
run("sudo bash -c 'echo -e \"#!/bin/bash\\nexec bspwm\" > /etc/lightdm/Xsession'")
run("sudo chmod +x /etc/lightdm/Xsession")

# Enable LightDM
run("sudo systemctl enable lightdm")

# Print message
print("Configuration is done. Please reboot your machine.")
