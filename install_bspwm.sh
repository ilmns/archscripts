#!/bin/bash

CONFIG_DIR="$HOME/.config"
BACKUP_DIR="$HOME/.config_backup"
WALLPAPER_DIR="/usr/share/backgrounds"
XINITRC_PATH="$HOME/.xinitrc"

install_required_packages() {
  local required_packages=("xorg-server" "bspwm" "sxhkd" "polybar" "picom" "feh" "rofi" "alacritty" "dmenu" "nitrogen" "lightdm")

  for package in "${required_packages[@]}"; do
    sudo pacman -S --noconfirm --needed "$package"
  done
}

create_config_dir() {
  local dirs=("$CONFIG_DIR/bspwm" "$CONFIG_DIR/sxhkd" "$CONFIG_DIR/rofi" "$CONFIG_DIR/picom" "$CONFIG_DIR/nitrogen")
  for dir in "${dirs[@]}"; do
    mkdir -p "$dir"
  done
}

copy_example_configs() {
  cp /usr/share/doc/bspwm/examples/bspwmrc $CONFIG_DIR/bspwm/bspwmrc
  cp /usr/share/doc/bspwm/examples/sxhkdrc $CONFIG_DIR/sxhkd/sxhkdrc
}

configure_picom() {
  echo -e "backend = \"glx\";\nvsync = true;" > "$CONFIG_DIR/picom/picom.conf"
}

configure_rofi() {
  echo -e "rofi.theme: Arc-Dark" > "$CONFIG_DIR/rofi/config.rasi"
}

configure_lightdm() {
  sudo sed -i 's/^#greeter-session=.*/greeter-session=lightdm-gtk-greeter/' /etc/lightdm/lightdm.conf
}

configure_nitrogen() {
  echo -e "[xin_-1]\nfile=/usr/share/backgrounds/default.jpg\nmode=5\nbgcolor=#000000" > "$CONFIG_DIR/nitrogen/bg-saved.cfg"
  nitrogen --restore
}

set_permissions() {
  chmod +x "$CONFIG_DIR/bspwm/bspwmrc"
  chmod +x "$CONFIG_DIR/sxhkd/sxhkdrc"
}

configure_xinit() {
  echo "exec bspwm" > "$XINITRC_PATH"
}

main() {
  install_required_packages
  create_config_dir
  copy_example_configs
  configure_picom
  configure_rofi
  configure_lightdm
  configure_nitrogen
  set_permissions
  configure_xinit
  sudo systemctl enable lightdm
  echo "Reboot your system to start using BSPWM."
}

main "$@"
