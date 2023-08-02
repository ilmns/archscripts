#!/bin/bash

# Function to update package lists and install Python and pip
install_python() {
    sudo pacman -Sy
    sudo pacman -S python python-pip
}

# Function to setup Python
setup_python() {
    # Create a .pythonrc file in the user's home directory
    PYTHONRC_PATH="$HOME/.pythonrc"

    # Contents of the .pythonrc file
    PYTHONRC_CONTENT='
# Enable auto-completion
try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

# Enable color support for ls
try:
    import os
    os.system("")
except:
    pass
'
    # Write the content to .pythonrc
    echo "$PYTHONRC_CONTENT" > $PYTHONRC_PATH

    # Add the .pythonrc file to .bashrc to run when a new shell opens
    echo "\n# Python personal configurations" >> $HOME/.bashrc
    echo "export PYTHONSTARTUP=$PYTHONRC_PATH" >> $HOME/.bashrc
}

install_python
setup_python

echo "Python installation and configuration completed."
