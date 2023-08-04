#!/bin/bash

# Function to check if running on Arch Linux-based system
check_arch_linux() {
    if [[ ! -x /usr/bin/pacman ]]; then
        echo "This script is intended for Arch Linux-based systems only."
        exit 1
    fi
}

# Function to check if the home directory is set
check_home_directory() {
    if [[ -z $HOME ]]; then
        echo "Home directory not set. Please make sure your HOME environment variable is set."
        exit 1
    fi
}

# Function to check if a directory exists or create it
check_or_create_directory() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
    fi
}

# Function to ask for sudo password
ask_sudo_password() {
    read -s -p "Please enter your sudo password: " sudo_password
    echo "$sudo_password"
}

# Function to install required packages
install_packages() {
    local packages=("bspwm" "sxhkd" "polybar" "dunst" "picom" "rofi" "thunar")
    sudo pacman -S --noconfirm "${packages[@]}" || {
        echo "Failed to install required packages."
        exit 1
    }
}

# Function to enable bspwm and sxhkd at start
enable_bspwm_and_sxhkd_at_start() {
    cat > "$HOME/.xinitrc" <<EOL
#!/bin/bash
sxhkd &
exec bspwm
EOL
    chmod +x "$HOME/.xinitrc"
}

# Function to set up autostart for bspwm and sxhkd in lightdm
setup_lightdm_autostart() {
    local config_dir="$HOME/.config"
    local autostart_dir="$config_dir/autostart"
    check_or_create_directory "$autostart_dir"

    cat > "$autostart_dir/bspwm.desktop" <<EOL
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
    cat > "$autostart_dir/sxhkd.desktop" <<EOL
[Desktop Entry]
Type=Application
Exec=sxhkd
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[fi_FI]=sxhkd
Name=sxhkd
Comment[fi_FI]=
Comment=
EOL

    sudo systemctl enable lightdm.service || {
        echo "Failed to enable lightdm service."
        exit 1
    }
}

# Function to write bspwm config
setup_bspwm() {
    local bspwm_dir="$HOME/.config/bspwm"
    check_or_create_directory "$bspwm_dir"

    cat > "$bspwm_dir/bspwmrc" <<EOL
#!/bin/bash

#!/bin/bash

# ----------------------------------------------------------------------------
# SET MONITORS AND DESKTOPS
# ----------------------------------------------------------------------------

# Create panels on each monitor
for m in $(bspc query -M --names); do
    bspc monitor "$m" -d 1 2 3 4 5 || {
        echo "Failed to create panels on monitor $m"
        exit 1
    }
done

# BSPWM CONFIGURATIONS
# ----------------------------------------------------------------------------
# Settings
bspc config border_width         2
bspc config window_gap           12
bspc config split_ratio          0.52
bspc config borderless_monocle   true
bspc config gapless_monocle      true
bspc config single_monocle       false
bspc config floating_enable      true

# Rules
bspc rule -a '*' center=on
bspc rule -a Steam state=floating

# Open Adobe Photoshop CS6 in a floating window
bspc rule -a Adobe\ Photoshop\ CS6 floating=on

bspc rule -a mpv \
     state=floating sticky=on follow=off focus=on \
     rectangle=640x360+2760+1040
bspc rule -a "*:Toolkit:Picture-in-Picture" \
     state=floating sticky=on follow=off focus=on \
     rectangle=640x360+2760+1040

# ----------------------------------------------------------------------------
# APPLICATION SHORTCUTS
# ----------------------------------------------------------------------------
# Open Thunar with "Super + T"
bspc bind super + t shell thunar

# Open Firefox Nightly with "Super + P"
bspc bind super + p shell firefox-nightly

# Toggle floating mode for the focused window
bspc bind super + shift + space node -t floating


# ----------------------------------------------------------------------------
# START DAEMONS AND UTILITIES
# ----------------------------------------------------------------------------
# Start sxhkd
sxhkd &

# Start compositor (picom)
picom -b &

# ----------------------------------------------------------------------------
# SET WALLPAPER
# ----------------------------------------------------------------------------
feh --bg-scale /home/crusader/Kuvat/WP/arch.png &

# ----------------------------------------------------------------------------
# START PANEL (POLYBAR)
# ----------------------------------------------------------------------------
"$HOME"/.config/polybar/launch.sh &

# ----------------------------------------------------------------------------
# START APPLICATIONS
# ----------------------------------------------------------------------------
lxqt-policykit-agent &

dunst &  # Notifications daemon
nm-applet &  # Network manager
eww daemon & # Eww 
volumeicon &  # Volume control for system tray
terminator &  # Terminal emulator

# Additional autostart applications
firefox-nightly &  # Web browser
telegram-desktop &  # Messaging app

# ----------------------------------------------------------------------------
# SET WM NAME
# ----------------------------------------------------------------------------
wmname LG3D

# ----------------------------------------------------------------------------
# EXECUTE BSPWM
# ----------------------------------------------------------------------------
exec bspwm


EOL
}

# Function to write sxhkd config
setup_sxhkd() {
    local sxhkd_dir="$HOME/.config/sxhkd"
    check_or_create_directory "$sxhkd_dir"

    cat > "$sxhkd_dir/sxhkdrc" <<EOL
# ------------------------------------------------------------------------------
# APPLICATION SHORTCUTS
# ------------------------------------------------------------------------------

# Launch Thunar (File Manager)
super + t
    thunar

# Launch Firefox
super + p
    firefox-nightly

# Launch Terminator (Terminal Emulator)
super + Return
    terminator

# Open a new terminal window
super + shift + Return
    terminator

# Launch Rofi in run mode
super + shift + d
    rofi -show run

# Launch Rofi in application menu mode
super + d
    rofi -show drun



# ------------------------------------------------------------------------------
# BSPWM CONTROLS
# ------------------------------------------------------------------------------

# Restart bspwm
super + Shift + r
    bspc wm -r

# Cycle through windows
super + Tab
    bspc node -f next.local

# Swap windows
super + shift + {h, j, k, l}
    bspc node -s {west, south, north, east}

# Window management
super + {_, shift + }{1-9, 0}
    bspc {desktop -f, node -d} '^{1-9, 10}'

super + {_, shift + }{h, j, k, l}
    bspc node -{f, s} {west, south, north, east}

# Tilting windows
super + y
    bspc node -t monocle

super + shift + y
    bspc node -t tiled

# Changing window size
super + alt + {h, j, k, l}
    bspc node -z {west -20 0, south 0 20, north 0 -20, east 20 0}

# Resize floating windows
super + ctrl + {h, j, k, l}
    bspc node -z {left -20 0, bottom 0 20, top 0 -20, right +20 0}

# Increase window size
super + period
    bspc node -z right +20 0 || bspc node -z bottom 0 -20

# Decrease window size
super + comma
    bspc node -z right -20 0 || bspc node -z bottom 0 20

# Move floating windows
super + ctrl + {Up, Down, Left, Right}
    bspc node -v {-20 0, 20 0, 0 -20, 0 20}

# Toggle floating window
super + shift + space
    bspc node -t ~floating

# Fibonacci tilting right
super + ctrl + l
    bspc node -R 90

# Close current window
super + q
    bspc node -c

# Fullscreen toggle
super + f
    bspc node -t fullscreen -T

# Toggle Polybar visibility
super + b
    /home/crusader/.config/polybar/toggle_polybar.sh

EOL
}

# Function to write polybar config
setup_polybar() {
    local polybar_dir="$HOME/.config/polybar"
    check_or_create_directory "$polybar_dir"

    cat > "$polybar_dir/config" <<EOL
# ... (Polybar config content here) ...
EOL
}

# Function to write dunst config
setup_dunst() {
    local dunst_dir="$HOME/.config/dunst"
    check_or_create_directory "$dunst_dir"

    cat > "$dunst_dir/dunstrc" <<EOL
# ... (Dunst config content here) ...
EOL
}

# Function to write picom config
setup_picom() {
    local picom_dir="$HOME/.config/picom"
    check_or_create_directory "$picom_dir"

    cat > "$picom_dir/picom.conf" <<EOL
# ------------------------------------------------------------------------------
# SHADOW
# ------------------------------------------------------------------------------

shadow = true;                   # Enable client-side shadows on windows.
shadow-radius = 10;              # The blur radius for shadows. (increased for softer shadows)
shadow-offset-x = -5;            # The left offset for shadows. (adjusted for better alignment)
shadow-offset-y = -5;            # The top offset for shadows. (adjusted for better alignment)
clear-shadow = true;             # Zero the part of the shadow's mask behind the window (experimental).

# Exclude windows from shadows
shadow-exclude = [
    "n:e:Notification",
    "n:e:Docky",
    "class_g = 'Conky'",
    "class_g ?= 'Notify-osd'",
    "class_g = 'Cairo-clock'",
    "_GTK_FRAME_EXTENTS@:c"
];

# ------------------------------------------------------------------------------
# FADING
# ------------------------------------------------------------------------------

fading = true;                   # Fade windows during opacity changes.
fade-delta = 10;                 # The time between steps in a fade in milliseconds.
fade-in-step = 0.03;             # Opacity change between steps while fading in.
fade-out-step = 0.03;            # Opacity change between steps while fading out.

# Fade windows in/out when opening/closing.
no-fading-openclose = false;    

# ------------------------------------------------------------------------------
# TRANSPARENCY
# ------------------------------------------------------------------------------

inactive-opacity = 0.9;          # Opacity of inactive windows. (0.0 - 1.0)
active-opacity = 1.0;            # Opacity of active windows. (0.0 - 1.0)
frame-opacity = 1.0;             # Opacity of window title bars and borders. (0.0 - 1.0)

# Enable to allow Picom to set the _NET_WM_OPACITY of inactive windows.
inactive-opacity-override = false;

# ------------------------------------------------------------------------------
# BACKEND
# ------------------------------------------------------------------------------

backend = "glx";                 # Use GLX (OpenGL) backend to draw window contents. Change to "xrender" if experiencing issues.

# ------------------------------------------------------------------------------
# VSYNC
# ------------------------------------------------------------------------------

vsync = true;                    # Enable vsync to avoid screen tearing, particularly for NVIDIA users.

# ------------------------------------------------------------------------------
# OTHER
# ------------------------------------------------------------------------------

detect-client-opacity = true;    # This prevents opacity being ignored for some apps. Set to false if it causes issues.

EOL
}

# Function to write rofi config
setup_rofi() {
    local rofi_dir="$HOME/.config/rofi"
    check_or_create_directory "$rofi_dir"

    cat > "$rofi_dir/config.rasi" <<EOL
@theme "/usr/share/rofi/themes/DarkBlue.rasi"
EOL
}



# Main function
main() {
    # Check if running on Arch Linux-based system
    check_arch_linux

    # Check if the home directory is set
    check_home_directory

    # Ask for sudo password and install packages
    sudo_password=$(ask_sudo_password)
    install_packages

    # Check if --dry-run option is given
    if [[ "$1" == "--dry-run" ]]; then
        echo "Dry run: No changes will be made."
        exit 0
    fi

    # Write configuration files
    enable_bspwm_and_sxhkd_at_start
    setup_lightdm_autostart
    setup_bspwm
    setup_sxhkd
    setup_polybar
    setup_dunst
    setup_picom
    setup_rofi
}

main "$@"
