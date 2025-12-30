import os
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
    Key must be a valid Fernet key (handled in config).
    """
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

    stored_name = f"{name}{version_suffix}{ext}"
    stored_path = os.path.join(upload_folder, stored_name)

    # 🔐 Encrypt file data
    data = file_storage.read()
    fernet = _get_fernet()
    encrypted = fernet.encrypt(data)

    with open(stored_path, "wb") as f_out:
        f_out.write(encrypted)

    return stored_path, stored_name


# =========================
# DECRYPT FILE
# =========================
def decrypt_file(filepath: str) -> bytes:
    with open(filepath, "rb") as f_in:
        encrypted = f_in.read()

    fernet = _get_fernet()

    try:
        return fernet.decrypt(encrypted)
    except InvalidToken:
        # If key mismatch or corrupted file
        raise RuntimeError("Unable to decrypt file. Invalid encryption key.")
