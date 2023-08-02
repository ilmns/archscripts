#!/bin/bash

# Define paths
home_dir=$HOME
config_dir="$home_dir/.config"
bspwm_dir="$config_dir/bspwm"
sxhkd_dir="$config_dir/sxhkd"
polybar_dir="$config_dir/polybar"
dunst_dir="$config_dir/dunst"
picom_dir="$config_dir/picom"
rofi_dir="$config_dir/rofi"
lightdm_config_dir="/etc/lightdm"
accountservice_dir="/var/lib/AccountsService/users"
zshrc_file="$home_dir/.zshrc"

# Create config directories
mkdir -p "$bspwm_dir" "$sxhkd_dir" "$polybar_dir" "$dunst_dir" "$picom_dir" "$rofi_dir" "$lightdm_config_dir" "$accountservice_dir"

# Define function to ask for sudo password
ask_sudo_password() {
    read -s -p "Please enter your sudo password: " sudo_password
    echo "$sudo_password"
}

# Install required packages
install_packages() {
    sudo_password="$1"
    packages=("zsh" "zsh-syntax-highlighting" "zsh-autosuggestions" "autojump" "git" "git-flow" "z" "history-substring-search" "colored-man-pages" "common-aliases" "colorize")
    for package in "${packages[@]}"; do
        echo "$sudo_password" | yay -S --noconfirm "$package"
        if [ $? -ne 0 ]; then
            echo "Error occurred during package installation: $package"
        fi
    done
}

# Change default shell to Zsh
change_default_shell() {
    if ! grep -q '/usr/bin/zsh' /etc/shells; then
        echo '/usr/bin/zsh' | sudo tee -a /etc/shells
    fi

    sudo chsh -s /usr/bin/zsh "$(whoami)"
}

# Write Zsh config
setup_zsh_config() {
    cat > "$zshrc_file" <<EOL
# Load Oh-My-Zsh framework
export ZSH="$home_dir/.oh-my-zsh"
ZSH_THEME="agnoster"
plugins=()

# Initialize Oh-My-Zsh
source "\$ZSH/oh-my-zsh.sh"

# Syntax highlighting
plugins+=(zsh-syntax-highlighting)

# Autosuggestions
plugins+=(zsh-autosuggestions)

# Zsh history substring search (press Up/Down to search history)
plugins+=(history-substring-search)

# Enhanced directory navigation with 'z' (jump around)
plugins+=(z)

# Command auto-correction
plugins+=(autojump)

# Git aliases and enhancements
plugins+=(git git-flow)

# Z - Jump to Frequent Directories
plugins+=(z)

# History search
plugins+=(history)

# Colored man pages
plugins+=(colored-man-pages)

# Common aliases
plugins+=(common-aliases)

# Colorize
plugins+=(colorize)

EOL
}

# Main function
main() {
    sudo_password=$(ask_sudo_password)
    install_packages "$sudo_password"
    change_default_shell
    setup_zsh_config
}

main
