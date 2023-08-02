#!/bin/bash

# Install required packages
sudo pacman -S --noconfirm bspwm sxhkd polybar picom dunst lightdm lightdm-gtk-greeter

# Define paths
home_dir=$HOME
config_dir="$home_dir/.config"
bspwm_dir="$config_dir/bspwm"
sxhkd_dir="$config_dir/sxhkd"
polybar_dir="$config_dir/polybar"
dunst_dir="$config_dir/dunst"
picom_dir="$config_dir/picom"
lightdm_config_dir="/etc/lightdm"
accountservice_dir="/var/lib/AccountsService/users"

bspwm_config_file="$bspwm_dir/bspwmrc"
sxhkd_config_file="$sxhkd_dir/sxhkdrc"
polybar_config_file="$polybar_dir/config"
dunst_config_file="$dunst_dir/dunstrc"
picom_config_file="$picom_dir/picom.conf"
bspwm_autostart_file="$home_dir/.xinitrc"
bspwm_desktop_file="$config_dir/autostart/bspwm.desktop"
accountservice_file="$accountservice_dir/$(whoami)"

# Create config directories
mkdir -p "$bspwm_dir" "$sxhkd_dir" "$polybar_dir" "$dunst_dir" "$picom_dir" "$lightdm_config_dir" "$accountservice_dir"

# Define function to ask for sudo password
ask_sudo_password() {
    read -s -p "Please enter your sudo password: " sudo_password
    echo "$sudo_password"
}

# Install required packages
install() {
    sudo_password="$1"
    packages=("bspwm" "sxhkd" "polybar" "dunst" "lightdm" "lightdm-gtk-greeter")
    for package in "${packages[@]}"; do
        echo "$sudo_password" | sudo -S pacman -S --noconfirm "$package"
        if [ $? -ne 0 ]; then
            echo "Error occurred during package installation: $package"
        fi
    done
}

# Configure bspwm and sxhkd
setup_bspwm_sxhkd() {
    # Sample bspwm config
    bspwm_config="#!/bin/bash\n\n# Create panels on each monitor\nfor m in \$(bspc query -M --names); do\n    bspc monitor \"\$m\" -d 1 2 3 4 5 || {\n        echo \"Failed to create panels on monitor \$m\"\n        exit 1\n    }\ndone\n\n# Continue the rest of the bspwm config contents\n"

    # Sample sxhkd config
    sxhkd_config="# Launch Thunar (File Manager)\nsuper + t\n    thunar\n\n# Launch Chromium\nsuper + p\n    chromium\n\n# Launch Terminator (Terminal Emulator)\nsuper + Return\n    terminator\n"

    # Write config files
    echo "$bspwm_config" > "$bspwm_config_file"
    echo "$sxhkd_config" > "$sxhkd_config_file"
}

# Configure polybar
setup_polybar() {
    # Sample polybar config
    polybar_config="[colors]\nbackground = #1a1b26\nforeground = #a9b1d6\nprimary = #7aa2f7\nsecondary = #9ece6a\nalert = #f7768e\n\n[bar/mybar]\nwidth = 100%\nheight = 27\nradius = 6.0\nfixed-center = false\n\nbackground = \${colors.background}\nforeground = \${colors.foreground}\n\nline-size = 3\nline-color = #f00\n\nborder-size = 4\nborder-color = #00000000\n\npadding-left = 0\npadding-right = 2\n\nfont-0 = fixed:pixelsize=10;1\nfont-1 = unifont:fontformat=truetype:size=8:antialias=false;0\nfont-2 = siji:pixelsize=10;1\n\nmodules-left = bspwm i3 xwindow\nmodules-center = mpd\nmodules-right = mpd alsa backlight xkeyboard memory cpu temperature battery eth date powermenu\n\ntray-position = right\ntray-padding = 2\n\ncursor-click = pointer\ncursor-scroll = ns-resize\n\n[module/xwindow]\ntype = internal/xwindow\nlabel = %title:0:30:...%\n\n[module/xkeyboard]\ntype = internal/xkeyboard\nblacklist-0 = num lock\n\nformat-prefix = \" \"\nformat-prefix-foreground = \${colors.foreground-alt}\nformat-prefix-underline = \${colors.secondary}\n\nlabel-layout = %layout%\nlabel-layout-underline = \${colors.secondary}\n\nlabel-indicator-padding = 2\nlabel-indicator-margin = 1\nlabel-indicator-background = \${colors.secondary}\nlabel-indicator-underline = \${colors.secondary}\n\n[module/filesystem]\ntype = internal/fs\ninterval = 25\n\nmount-0 = /\n\nlabel-mounted = %\{F#0a81f5\}%mountpoint%%\{F-\}: %percentage_used%%\nlabel-unmounted = %mountpoint% not mounted\nlabel-unmounted-foreground = \${colors.foreground-alt}\n\n[module/bspwm]\ntype = internal/bspwm\n\nlabel-focused = %index%\nlabel-focused-background = \${colors.background-alt}\nlabel-focused-underline= \${colors.primary}\nlabel-focused-padding = 2\n\nlabel-occupied = %index%\nlabel-occupied-padding = 2\n\nlabel-urgent = %index%!\nlabel-urgent-background = \${colors.alert}\nlabel-urgent-padding = 2\n\nlabel-empty = %index%\nlabel-empty-foreground = \${colors.foreground-alt}\nlabel-empty-padding = 2\n\n[module/i3]\ntype = internal/i3\nformat = <label-state> <label-mode>\nindex-sort = true\nwrapping-scroll = false\n\nlabel-mode-padding = 2\nlabel-mode-foreground = #000\nlabel-mode-background = \${colors.primary}\n\nlabel-focused = %index%\nlabel-focused-background = \${colors.background-alt}\nlabel-focused-underline= \${colors.primary}\nlabel-focused-padding = 2\n\nlabel-unfocused = %index%\nlabel-unfocused-padding = 2\n\nlabel-visible = %index%\nlabel-visible-background = \${self.label-focused-background}\nlabel-visible-underline = \${self.label-focused-underline}\nlabel-visible-padding = \${self.label-focused-padding}\n\nlabel-urgent = %index%\nlabel-urgent-background = \${colors.alert}\nlabel-urgent-padding = 2\n"

    # Write config file
    echo -e "$polybar_config" > "$polybar_config_file"
}

# Configure dunst
setup_dunst() {
    # Sample dunst config
    dunst_config="[global]\nfont = Monospace 9\nformat = \"%s: %b\"\nindicate_hidden = true\nstack_duplicates = true\nstartup_notification = true\nmonitor = 0\n\n[urgency_low]\nforeground = \"#a9b1d6\"\nbackground = \"#1a1b26\"\n\n[urgency_normal]\nforeground = \"#a9b1d6\"\nbackground = \"#1a1b26\"\n\n[urgency_critical]\nforeground = \"#a9b1d6\"\nbackground = \"#1a1b26\"\n"

    # Write config file
    echo -e "$dunst_config" > "$dunst_config_file"
}

# Configure picom
setup_picom() {
    # Sample picom config
    picom_config="# Basic Options\nbackend = \"glx\";\nvsync = true;\nno-dock-shadow = true;\nno-dnd-shadow = true;\nunredir-if-possible = true;\nfocus-exclude = [ \"class_g ?= 'Conky'\", \"class_g ?= 'polybar'\" ];\ndetect-rounded-corners = true;\ndetect-client-opacity = true;\n\n# Opacity Options\ninactive-opacity = 0.9;\nframe-opacity = 1.0;\ninactive-opacity-override = true;\nalpha-step = 0.06;\n\n# Shadows\nshadow = false;\nshadow-radius = 10;\nshadow-offset-x = -15;\nshadow-offset-y = -15;\nshadow-exclude = [\n    \"class_g ?= 'TelegramDesktop'\",\n    \"class_g ?= 'discord'\"\n];\n\n# Fading\nfade-in-step = 0.03;\nfade-out-step = 0.03;\nfade-exclude = [ ];\n\n# Blur\nblur-background = true;\nblur-background-frame = true;\nblur-background-fixed = true;\nblur-kern = \"9x9box\";\nblur-background-exclude = [\n    \"window_type = 'dock'\",\n    \"window_type = 'desktop'\",\n    \"_GTK_FRAME_EXTENTS@:c\"\n];\n"

    # Write config file
    echo -e "$picom_config" > "$picom_config_file"
}

# Enable bspwm at start
enable_bspwm_at_start() {
    echo -e "\nexec bspwm\n" >> "$bspwm_autostart_file"

    desktop_file_content="[Desktop Entry]\nType=Application\nExec=bspwm\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName[fi_FI]=bspwm\nName=bspwm\nComment[fi_FI]=\nComment=\n"
    bspwm_desktop_dir="$config_dir/autostart"
    mkdir -p "$bspwm_desktop_dir"

    echo -e "$desktop_file_content" > "$bspwm_desktop_file"
    sudo systemctl enable lightdm.service
}

main() {
    sudo_password=$(ask_sudo_password)
    install "$sudo_password"
    setup_bspwm_sxhkd
    setup_polybar
    setup_dunst
    setup_picom
    enable_bspwm_at_start
}

main
