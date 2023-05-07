#!/bin/bash

# Define colors for messages
BLACK='\e[48;5;0m\e[38;5;255m'
RED='\e[48;5;160m\e[38;5;255m'
GREEN='\e[48;5;40m\e[38;5;255m'
BLUE='\e[48;5;27m\e[38;5;255m'
MAGENTA='\e[48;5;164m\e[38;5;255m'
CYAN='\e[48;5;37m\e[38;5;255m'
WHITE='\e[48;5;15m\e[38;5;0m'
NC='\e[0m'
YELLOW='\e[48;5;226m\e[38;5;0m'

# Function to install packages with Yay
function install_package() {
    package="$1"
    echo -e "${CYAN}Installing package $package...${NC}"
    if yay -S --noconfirm "$package"; then
        echo -e "${GREEN}$package installed successfully!${NC}"
    else
        echo -e "${RED}Failed to install $package.${NC}"
        exit 1
    fi
}

# Update system and install yay if not installed
echo -e "${BLUE}Updating system and installing Yay...${NC}"
if sudo pacman -Syyu --noconfirm && command -v yay &> /dev/null || sudo pacman -S yay --noconfirm; then
    echo -e "${GREEN}System updated and Yay installed successfully!${NC}"
else
    echo -e "${RED}Failed to update system or install Yay.${NC}"
    exit 1
fi

# Install recommended and most common Vim packages from Yay
echo -e "${BLUE}Installing recommended and most common Vim packages from Yay...${NC}"
for package in vim vim-plug fzf fzf.vim the_silver_searcher; do
    install_package "$package"
done
echo -e "${GREEN}Vim packages installed successfully!${NC}"

# Inform user about Vim plugins and settings
echo -e "${BLUE}The following Vim plugins have been installed:${NC}"
echo "- vim-sensible: a set of default options for Vim"
echo "- vim-fugitive: a Git wrapper for Vim"
echo "- vim-gitgutter: shows a Git diff in the gutter"
echo "- fzf: a command-line fuzzy finder"
echo "- fzf.vim: integrates fzf with Vim"
echo "- the_silver_searcher: a fast code-searching tool"
echo ""
echo -e "${BLUE}The following settings have been added to your .vimrc file:${NC}"
echo "- Tabstop, softtabstop, and shiftwidth set to 4"
echo "- Expandtab enabled"
echo "- hlsearch and incsearch enabled"
echo "- Line numbers and cursorline enabled"
echo "- Showmatch and ignorecase enabled"
echo "- Smartcase enabled"
echo "- Laststatus set to 2"
echo "- Gruvbox color scheme enabled"
echo ""
echo -e "${BLUE}If you want to install additional Vim plugins, add them to your .vimrc file and run 'vim +PlugInstall'.${NC}"
echo ""

# Prompt user for color theme preference
read -p "$(echo -e "${BLUE}Choose a color theme for Vim (dark/light): ${NC}")" theme
while [[ ! $theme =~ ^(dark|light)$ ]]; do
    echo -e "${RED}Invalid input. Please enter 'dark' or 'light'.${NC}"
    read -p "$(echo -e "${BLUE}Choose a color theme for Vim (dark/light): ${NC}")" theme
done


# Update .vimrc with the selected color theme
if [ "$theme" == "dark" ]; then
    echo "colorscheme gruvbox" >> ~/.vimrc
    echo "set background=dark" >> ~/.vimrc
else
    echo "colorscheme gruvbox" >> ~/.vimrc
    echo "set background=light" >> ~/.vimrc
fi



    read -p "$(echo -e "${BLUE}Do you want to activate the Vim settings now? [y/n]: ${NC}")" answer
if [[ $answer =~ ^[Yy]$ ]]; then
    vim +PlugInstall +qall
    echo -e "${GREEN}Vim settings activated successfully!${NC}"
else
    echo -e "${YELLOW}Vim settings not activated.${NC}"
fi

echo -e "${GREEN}All done! Enjoy using Vim.${NC}"
