#!/bin/bash

# Define variables
INSTALL_DIR="$HOME/sbin"
SCRIPT_NAME="releases.py"
TARGET_SCRIPT_NAME="releases"  # The name without .py suffix for installation
REQUIREMENTS_FILE="requirements.txt"
TEMP_PY_SCRIPT="generate_reqs.py"

# Ensure Python and pip are installed
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "Python3 or pip3 is not installed. Please install them before continuing."
    exit 1
fi

# Create installation directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy and rename the script
cp "$SCRIPT_NAME" "$INSTALL_DIR/$TARGET_SCRIPT_NAME"
chmod +x "$INSTALL_DIR/$TARGET_SCRIPT_NAME"

# Install Python dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing Python dependencies from $REQUIREMENTS_FILE..."
    pip3 install -r "$REQUIREMENTS_FILE"
else
    echo "No $REQUIREMENTS_FILE found. Skipping Python dependencies installation."
fi

# Function to update PATH in the appropriate shell configuration file
update_path() {
    local shell_config_file="$1"
    if ! grep -q 'export PATH="$HOME/sbin:$PATH"' "$shell_config_file" ; then
        echo 'export PATH="$HOME/sbin:$PATH"' >> "$shell_config_file"
        echo "Updated $shell_config_file with new PATH."
    else
        echo "PATH already correctly set in $shell_config_file."
    fi
}

# Detecting the shell and updating the correct configuration file
SHELL_TYPE=$(basename "$SHELL")

case "$SHELL_TYPE" in
bash)
    update_path "$HOME/.bashrc"
    ;;
zsh)
    update_path "$HOME/.zshrc"
    ;;
*)
    echo "Unsupported shell: $SHELL_TYPE. Please manually update your PATH."
    ;;
esac

echo "Installation completed. The script is available at $INSTALL_DIR/$TARGET_SCRIPT_NAME"
echo "Please restart your terminal or source your shell configuration file for the PATH update to take effect."

