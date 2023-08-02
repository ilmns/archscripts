#!/bin/bash

# Install required packages
install_packages() {
    local packages=("bspwm" "sxhkd" "polybar" "dunst" "picom" "lightdm" "lightdm-gtk-greeter" "rofi" "thunar")
    sudo pacman -S --noconfirm "${packages[@]}"
}

# Define paths
home_dir="$HOME"
config_dir="$home_dir/.config"
bspwm_dir="$config_dir/bspwm"
sxhkd_dir="$config_dir/sxhkd"
polybar_dir="$config_dir/polybar"
dunst_dir="$config_dir/dunst"
picom_dir="$config_dir/picom"
rofi_dir="$config_dir/rofi"
lightdm_config_dir="/etc/lightdm"
accountservice_dir="/var/lib/AccountsService/users"

# Create config directories
mkdir -p "$bspwm_dir" "$sxhkd_dir" "$polybar_dir" "$dunst_dir" "$picom_dir" "$rofi_dir" "$lightdm_config_dir" "$accountservice_dir"

# Define function to ask for sudo password
ask_sudo_password() {
    read -s -p "Please enter your sudo password: " sudo_password
    echo "$sudo_password"
}

# Install required packages
install() {
    local sudo_password="$1"
    install_packages
}

# Write bspwm config
setup_bspwm() {
    cat > "$bspwm_dir/bspwmrc" <<EOL
#!/bin/bash

# Launch Thunar
thunar &

# Create panels on each monitor
for m in \$(bspc query -M --names); do
    bspc monitor "\$m" -d 1 2 3 4 5 || {
        echo "Failed to create panels on monitor \$m"
        exit 1
    }
done

# Continue the rest of the bspwm config contents
EOL
}
# Write sxhkd config
setup_sxhkd() {
    cat > "$sxhkd_dir/sxhkdrc" <<EOL
# Launch Thunar (File Manager)
super + t
    thunar

# Launch Chromium
super + p
    chromium

# Launch Terminator (Terminal Emulator)
super + Return
    terminator
EOL
}

# Write sxhkd config
setup_sxhkd() {
    cat > "$sxhkd_dir/sxhkdrc" <<EOL
# Launch Thunar (File Manager)
super + t
    thunar

# Launch Chromium
super + p
    chromium

# Launch Terminator (Terminal Emulator)
super + Return
    terminator
EOL
}

# Write polybar config
setup_polybar() {
    cat > "$polybar_dir/config" <<EOL
# Polybar config content here
EOL
}

# Write dunst config
setup_dunst() {
    cat > "$dunst_dir/dunstrc" <<EOL
# Dunst config content here
EOL
}

# Write picom config
setup_picom() {
    cat > "$picom_dir/picom.conf" <<EOL
# Picom config content here
EOL
}

# Write rofi config
setup_rofi() {
    cat > "$rofi_dir/config" <<EOL
# Rofi config content here
EOL
}


# Enable bspwm at start
enable_bspwm_at_start() {
    cat > "$home_dir/.xinitrc" <<EOL
#!/bin/bash
exec bspwm
EOL

    cat > "$config_dir/autostart/bspwm.desktop" <<EOL
[Desktop Entry]
Type=Application
Exec=bspwm
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[fi_FI]=bspwm
Name=bspwm
Comment[fi_FI]=
Comment=
EOL

    sudo systemctl enable lightdm.service
}

# Main function
main() {
    sudo_password=$(ask_sudo_password)
    install "$sudo_password"
    setup_bspwm
    setup_sxhkd
    setup_polybar
    setup_dunst
    setup_picom
    setup_rofi
    enable_bspwm_at_start
}

main
