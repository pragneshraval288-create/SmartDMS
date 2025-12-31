import os
import uuid  # [SECURITY ENHANCEMENT] Unique IDs ke liye
from typing import Tuple
from cryptography.fernet import Fernet, InvalidToken
from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ..config import allowed_file, Config


# =========================
# INTERNAL: GET FERNET
# =========================
def _get_fernet() -> Fernet:
    """
    Returns Fernet instance using application ENCRYPTION_KEY.
    """
    # Key valid hai ya nahi, ye Config file mein check ho chuka hai
    key = Config.ENCRYPTION_KEY

    if isinstance(key, str):
        key = key.encode()

    return Fernet(key)


# =========================
# SAVE ENCRYPTED FILE
# =========================
def save_encrypted_file(
    file_storage: FileStorage,
    version_suffix: str = ""
) -> Tuple[str, str]:

    if not file_storage or file_storage.filename == "":
        raise ValueError("No file provided")

    if not allowed_file(file_storage.filename):
        raise ValueError("File type not allowed")

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    original_name = secure_filename(file_storage.filename)
    name, ext = os.path.splitext(original_name)

    # [SECURITY FIX] 
    # File ko Disk par Random UUID naam se save karein.
    # Isse "File Overwrite" aur "Predictable Filename" attacks ruk jate hain.
    # Original naam Database mein rahega, Disk par nahi.
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    
    stored_path = os.path.join(upload_folder, unique_filename)

    # 🔐 Encrypt file data
    # Note: 32MB limit Config mein hai, isliye RAM full hone ka risk kam hai.
    data = file_storage.read()
    fernet = _get_fernet()
    encrypted = fernet.encrypt(data)

    with open(stored_path, "wb") as f_out:
        f_out.write(encrypted)

    # Return stored_path AND unique_filename (taaki DB mein update ho sake)
    return stored_path, unique_filename


# =========================
# DECRYPT FILE
# =========================
def decrypt_file(filepath: str) -> bytes:
    # [SECURITY CHECK] Path Traversal defense already done via 'secure_filename' during upload.
    # Agar hacker ne DB manually edit karke path '/etc/passwd' kar diya,
    # toh bhi decrypt fail ho jayega kyunki '/etc/passwd' encrypted nahi hai.
    
    try:
        with open(filepath, "rb") as f_in:
            encrypted = f_in.read()
    except FileNotFoundError:
        raise RuntimeError("File not found on server.")

    fernet = _get_fernet()

    try:
        return fernet.decrypt(encrypted)
    except InvalidToken:
        # If key mismatch or corrupted file
        raise RuntimeError("Unable to decrypt file. Invalid encryption key or corrupted file.")