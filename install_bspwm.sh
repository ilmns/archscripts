#!/bin/bash

CONFIG_DIR="$HOME/.config"
BACKUP_DIR="$HOME/.config_backup"
WALLPAPER_DIR="/usr/share/backgrounds"
XINITRC_PATH="$HOME/.xinitrc"

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --path)
        path="$2"
        shift 2
        ;;
      --url)
        url="$2"
        shift 2
        ;;
      --random)
        random=true
        shift
        ;;
      *)
        echo "Invalid option: $1"
        exit 1
        ;;
    esac
  done
}

download() {
  local url="$1"
  local path="$2"
  if command -v curl &>/dev/null; then
    curl -s -L -o "$path" "$url"
  elif command -v wget &>/dev/null; then
    wget -q "$url" -O "$path"
  else
    echo "Error: Neither curl nor wget is installed. Cannot download wallpaper."
    exit 1
  fi
}

print_color() {
  local msg="$1"
  local code="$2"
  echo -e "\033[${code}m${msg}\033[0m"
}

exec_command() {
  if "$@"; then
    return 0
  else
    echo "Error executing command: $*"
    return 1
  fi
}

package_installed() {
  local pkg="$1"
  if exec_command pacman -Q "$pkg" &>/dev/null; then
    return 0
  else
    return 1
  fi
}

install() {
  local pkg="$1"
  if package_installed "$pkg"; then
    print_color "$pkg is already installed. Skipping..." "1;33"
  else
    if exec_command sudo pacman -S --noconfirm "$pkg"; then
      print_color "$pkg installed successfully." "1;32"
    else
      print_color "Failed to install $pkg." "1;31"
    fi
  fi
}

make_dir() {
  local path="$1"
  if [[ ! -d "$path" ]]; then
    mkdir -p "$path"
  fi
}

set_wallpaper() {
  local path="$1"
  local url="$2"
  local random="$3"

  if [[ $random == true ]]; then
    local img_paths=()
    while IFS= read -r -d '' file; do
      img_paths+=("$file")
    done < <(find "$WALLPAPER_DIR" -type f \( -iname "*.jpg" -o -iname "*.png" \) -print0)

    if [[ ${#img_paths[@]} -eq 0 ]]; then
      echo "Warning: No wallpaper files found in $WALLPAPER_DIR."
      return
    fi

    local random_img
    random_img=${img_paths[RANDOM % ${#img_paths[@]}]}
    feh --bg-scale "$random_img"
  elif [[ -n $url ]]; then
    download "$url" "$path"
    feh --bg-scale "$path"
  else
    echo "Error: No wallpaper specified."
    return
  fi
}

handle_file() {
  local path="$1"
  local content="$2"

  if [[ -f "$path" ]]; then
    if ! create_backup "$path"; then
      echo "Failed to create backup: $path"
      return 1
    fi
  fi
  echo "$content" > "$path"
  print_color "$path written." "1;32"
}

create_backup() {
  local path="$1"
  local backup_name
  backup_name="$(basename "$path").$(date +"%Y%m%d%H%M%S").bak"
  local backup_path="$BACKUP_DIR/$backup_name"
  if cp "$path" "$backup_path"; then
    print_color "Created backup: $backup_name" "1;32"
    return 0
  else
    print_color "Failed to create backup: $backup_name" "1;33"
    return 1
  fi
}

setup_bspwm() {
  parse_args "$@"

  make_dir "$BACKUP_DIR"

  local required_packages=("xorg-server" "bspwm" "sxhkd" "polybar" "picom" "feh" "rofi" "alacritty" "dmenu" "nitrogen")

  for package in "${required_packages[@]}"; do
    install "$package"
  done

  set_wallpaper "$path" "$url" "$random"

  local bspwmrc_content="#!/bin/bash
sxhkd &
polybar bspwm &
picom -b &
exec bspwm
"

  local sxhkdrc_content="super + Return
  alacritty
super + Shift + q
  bspc window -c
super + {h,j,k,l}
  bspc node -{focus,shift} {west,south,north,east}
super + {Left,Down,Up,Right}
  bspc node -{focus,shift} {west,south,north,east}
super + d
  rofi -show drun
"

  local xinitrc_content="exec bspwm"

  handle_file "$CONFIG_DIR/bspwm/bspwmrc" "$bspwmrc_content"
  handle_file "$CONFIG_DIR/sxhkd/sxhkdrc" "$sxhkdrc_content"
  handle_file "$XINITRC_PATH" "$xinitrc_content"

  chmod +x "$CONFIG_DIR/bspwm/bspwmrc"
  print_color "bspwm setup completed. Restart your session for changes to take effect." "1;32"
}

setup_bspwm "$@"
