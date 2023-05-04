#!/bin/bash
#
# This script installs Git and CMake if they are not already installed, then installs
# the necessary dependencies and clones the Polybar repository. It then builds and installs
# Polybar, creates a default configuration file in the ~/.config/polybar directory,
# configures the launch script to start on login, and starts Polybar.

# Install Git and CMake if not installed
if ! command -v git &> /dev/null; then
    echo "Git not found. Installing..."
    sudo pacman -S --noconfirm git
fi

if ! command -v cmake &> /dev/null; then
    echo "CMake not found. Installing..."
    sudo pacman -S --noconfirm cmake
fi

# Install dependencies
sudo pacman -S --noconfirm cairo xcb-util xcb-util-wm xcb-util-xrm pulseaudio \
  wireless_tools alsa-lib libmpdclient jsoncpp curl

# Clone the Polybar repository
if [ ! -d "polybar" ]; then
    git clone https://github.com/polybar/polybar.git
fi

# Build and install Polybar
cd polybar
mkdir -p build
cd build
cmake ..
make -j$(nproc)
sudo make install

# Configure Polybar
if [ ! -d "$HOME/.config/polybar" ]; then
    mkdir -p "$HOME/.config/polybar"
fi

if [ ! -f "$HOME/.config/polybar/config.ini" ]; then
    cat > "$HOME/.config/polybar/config.ini" <<EOF
[global/wm]
name = bspwm

[bar/top]
monitor = ${MONITOR:-DP-0}
modules-left =
modules-center = windowmanager
modules-right = date

[module/windowmanager]
type = internal/windowmanager
format = <label-focused>
label-focused = %title%
EOF
fi

if [ ! -f "$HOME/.config/polybar/launch.sh" ]; then
    cat > "$HOME/.config/polybar/launch.sh" <<EOF
#!/bin/bash
killall -q polybar
while pgrep -u \$UID -x polybar >/dev/null; do sleep 1; done
polybar top &
EOF
    chmod +x "$HOME/.config/polybar/launch.sh"
fi

# Configure Polybar to start on login
if [ ! -d "$HOME/.config/autostart" ]; then
    mkdir -p "$HOME/.config/autostart"
fi

if [ ! -f "$HOME/.config/autostart/polybar.desktop" ]; then
    cat > "$HOME/.config/autostart/polybar.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Polybar
Exec=bash \$HOME/.config/polybar/launch.sh
EOF
fi

# Start Polybar
"$HOME/.config/polybar/launch.sh"
