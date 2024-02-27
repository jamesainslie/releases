This setup consists of a Python script named `releases.py` and an installation Bash script named `install.sh`. The Python script is designed to automate the process of deploying applications to GitHub Container Registry (GHCR) with optional version management features. It includes functionalities such as Docker build and push operations, version incrementing, and automatic login to GHCR using a provided token. The accompanying Bash script automates the installation of this Python script into a user's system, including setting up necessary Python dependencies and ensuring the script is easily executable from anywhere in the system.

### What It Does:

#### `releases.py`:
- **Docker Operations**: It can build Docker images with optional no-cache options, tag them, and push them to GHCR under the user's account.
- **Version Management**: Allows specifying a release version or interactively updating the version based on major, minor, and patch increments.
- **GHCR Authentication**: Automates the login process to GHCR using a provided token.
- **Script Installation**: Offers an option to self-install the script into the user's system for easy access.
- **Configuration Management**: Creates a default configuration directory and file for storing user and token information.

#### `install.sh`:
- Ensures Python and pip are installed.
- Copies the Python script to a specified directory (`~/sbin`) and renames it for easier access.
- Installs any Python dependencies listed in a `requirements.txt` file.
- Updates the user's PATH environment variable to include the installation directory, ensuring the script can be run from anywhere.

### How to Install:

1. **Prepare Your Environment**:
   - Ensure you have Python 3 and pip installed on your system.
   - Have Docker installed if you plan to use the Docker functionalities of the script.
   - Download or clone the `releases.py` and `install.sh` scripts to your local machine.

2. **Run the Installation Script**:
   - Open a terminal and navigate to the directory containing `install.sh`.
   - Make the installation script executable: `chmod +x install.sh`.
   - Run the installation script: `./install.sh`.

### How to Use:

After installation, you can use the `releases` command (previously `releases.py`, now installed as `releases` for convenience) with various options:

- **Deploy a Docker Image**:
  ```bash
  releases --ghcr-user <your-ghcr-username> --token <your-ghcr-token> --release <version>
  ```
  Replace `<your-ghcr-username>`, `<your-ghcr-token>`, and `<version>` with your GitHub Container Registry username, your personal access token, and the release version you want to deploy, respectively.

- **Increment Version Interactively**:
  If you don't specify a version with `--release`, the script will prompt you to optionally increment the major, minor, or patch version based on the current version.

- **Install the Script** (If not done already):
  You can also use the `--install` flag with the Python script itself to perform a similar installation process to what `install.sh` does:
  ```bash
  python3 releases.py --install
  ```

### Important Notes:
- **GHCR Token**: For operations involving GHCR, you'll need a personal access token with appropriate permissions. You can generate this in your GitHub settings.
- **Docker Dependency**: Ensure Docker is running on your system if you intend to use the Docker-related features.
- **Configuration**: The script creates a `.releases` directory and a `releases.yaml` configuration file for storing user-specific settings. This is useful for avoiding the need to repeatedly enter the same information.

This setup simplifies the process of deploying applications and managing versions, making it an efficient tool for developers working with Docker and GitHub Container Registry.
