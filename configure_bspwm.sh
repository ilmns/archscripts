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

dep_check() {
  local dep="$1"
  if ! command -v "$dep" &>/dev/null; then
    print_color "$dep is missing. Installing it..." "1;33"
    install "$dep"
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

overwrite_prompt() {
  local path="$1"
  read -rp "$path already exists. Do you want to overwrite it? (yes/no): " response
  case $response in
    [Yy]|[Yy][Ee][Ss]) return 0 ;;
    *) return 1 ;;
  esac
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
    if overwrite_prompt "$path"; then
      create_backup "$path"
      echo "$content" > "$path"
      print_color "$path overwritten." "1;32"
    else
      print_color "$path not overwritten. Skipped." "1;33"
    fi
  else
    echo "$content" > "$path"
    print_color "$path created." "1;32"
  fi
}

create_backup() {
  local path="$1"
  local backup_name
  backup_name="$(basename "$path").$(date +"%Y%m%d%H%M%S").bak"
  local backup_path="$BACKUP_DIR/$backup_name"
  if cp "$path" "$backup_path"; then
    print_color "Created backup: $backup_name" "1;32"
  else
    print_color "Failed to create backup: $backup_name" "1;33"
  fi
}

set_default_shell() {
  local shell_options=("bash" "zsh" "fish")
  local default_shell=$(choose "${shell_options[@]}" "Select default shell:")
  case $default_shell in
    "bash")
      handle_file "$HOME/.bashrc" "exec bspwm"
      ;;
    "zsh")
      handle_file "$HOME/.zshrc" "exec bspwm"
      ;;
    "fish")
      handle_file "$CONFIG_DIR/fish/config.fish" "exec bspwm"
      ;;
  esac
}

choose() {
  local choices=("$@")
  local msg="$1"
  local i=1
  echo "$msg"
  for choice in "${choices[@]}"; do
    echo "$i. $choice"
    ((i++))
  done
  while true; do
    read -rp "> " choice </dev/tty
    if ((choice >= 1 && choice <= ${#choices[@]})); then
      echo "${choices[choice - 1]}"
      break
    else
      echo "Invalid choice. Please enter a number between 1 and ${#choices[@]}."
    fi
  done
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

  local rofi_config_content="rofi.theme: Arc-Dark
"

  local picom_config_content="backend = \"glx\";
vsync = true;
"

  make_dir "$CONFIG_DIR/bspwm"
  make_dir "$CONFIG_DIR/sxhkd"
  make_dir "$CONFIG_DIR/rofi"
  make_dir "$CONFIG_DIR/picom"

  handle_file "$CONFIG_DIR/bspwm/bspwmrc" "$bspwmrc_content"
  handle_file "$CONFIG_DIR/sxhkd/sxhkdrc" "$sxhkdrc_content"
  handle_file "$CONFIG_DIR/rofi/config.rasi" "$rofi_config_content"
  handle_file "$CONFIG_DIR/picom/picom.conf" "$picom_config_content"

  handle_file "$XINITRC_PATH" "#!/bin/sh\nexec bspwm"

  # Set default shell startup file
  set_default_shell

  # Check if the default shell startup file is set
  if [[ ! -f "$XINITRC_PATH" ]]; then
    echo "Error: Default shell startup file ($XINITRC_PATH) is missing."
    exit 1
  fi

  # Start bspwm
  startx
  exit 0
}

main() {
  setup_bspwm "$@"
}

main "$@"
