#!/bin/bash

# Define colors for messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Define functions for the script
check_git_installed() {
    if command -v git &> /dev/null; then
        echo -e "${GREEN}Git is already installed.${NC}"
    else
        echo -e "${RED}Git is not installed.${NC}"
    fi
}

install_git() {
    if command -v git &> /dev/null; then
        echo -e "${GREEN}Git is already installed.${NC}"
    else
        echo -e "${YELLOW}Installing Git...${NC}"
        sudo apt-get update
        sudo apt-get install git -y
        echo -e "${GREEN}Git installed successfully!${NC}"
    fi
}

configure_git() {
    read -p "Enter your name for Git commits: " name
    read -p "Enter your email for Git commits: " email
    git config --global user.name "$name"
    git config --global user.email "$email"
    echo -e "${GREEN}Git user name and email configured successfully!${NC}"
}

clone_repository() {
    read -p "Enter the URL of the repository to clone: " url
    git clone "$url"
    echo -e "${GREEN}Git repository cloned successfully!${NC}"
}

commit_changes() {
    read -p "Enter the path of the repository to commit changes: " path
    cd "$path"
    git add .
    read -p "Enter a commit message: " message
    git commit -m "$message"
    echo -e "${GREEN}Changes committed successfully!${NC}"
}

push_changes() {
    read -p "Enter the path of the repository to push changes: " path
    cd "$path"
    git push
    echo -e "${GREEN}Changes pushed successfully!${NC}"
}

open_repository() {
    read -p "Enter the path of the repository to open: " path
    cd "$path"
    xdg-open .
    echo -e "${GREEN}Repository opened successfully!${NC}"
}

clean_repository() {
    git_command_with_confirm "clean" "Are you sure you want to delete all untracked files?"
}

revert_repository() {
    git_command_with_confirm "reset --hard" "Are you sure you want to revert all changes?"
}

fetch_repository() {
    git_command "fetch"
}

pull_repository() {
    git_command "pull"
}

git_command() {
    read -p "Enter the path of the repository to run Git command: " path
    cd "$path"
    git $1
    echo -e "${GREEN}Git command '$1' executed successfully!${NC}"
}

git_command_with_confirm() {
    read -p "Enter the path of the repository to run Git command: " path
    cd "$path"
    read -p "$2 [y/N] " choice
    case "$choice" in 
        y|Y ) {
            git $1
            echo -e "${GREEN}Git command '$1' executed successfully!${NC}"
        }
            ;;
        * )
            echo -e "${YELLOW}Git command not executed.${NC}"
            ;;
    esac

}

save_settings() {
    echo "Saving Git settings..."
    git config --list > git_settings.txt
    echo -e "${GREEN}Git settings saved to git_settings.txt!${NC}"
}

# Main menu loop
while true; do
    echo "Please select an option:"
    echo -e "1. ${YELLOW}Check if Git is installed${NC}"
    echo -e "2. ${YELLOW}Install Git${NC}"
    echo -e "3. ${YELLOW}Configure Git user name and email${NC}"
    echo -e "4. ${YELLOW}Clone a Git repository${NC}"
    echo -e "5. ${YELLOW}Commit changes in a Git repository${NC}"
    echo -e "6. ${YELLOW}Push changes in a Git repository${NC}"
    echo -e "7. ${YELLOW}Check status of a Git repository${NC}"
    echo -e "8. ${YELLOW}Open a Git repository${NC}"
    echo -e "9. ${YELLOW}Clean a Git repository${NC}"
    echo -e "10. ${YELLOW}Revert a Git repository${NC}"
    echo -e "11. ${YELLOW}Fetch changes in a Git repository${NC}"
    echo -e "12. ${YELLOW}Pull changes in a Git repository${NC}"
    echo -e "13. ${YELLOW}Save Git settings${NC}"
    echo -e "14. ${YELLOW}Exit${NC}"

    read choice
    case $choice in
        1)
            check_git_installed
            ;;
        2)
            install_git
            ;;
        3)
            configure_git
            ;;
        4)
            clone_repository
            ;;
        5)
            commit_changes
            ;;
        6)
            push_changes
            ;;
        7)
            git_command "status"
            ;;
        8)
            open_repository
            ;;
        9)
            clean_repository
            ;;
        10)
            revert_repository
            ;;
        11)
            fetch_repository
            ;;
        12)
            pull_repository
            ;;
        13)
            save_settings
            ;;
        14)
            echo -e "${YELLOW}Exiting Git Manager.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac

    echo ""
done
