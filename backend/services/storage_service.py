import os
from typing import Tuple
from cryptography.fernet import Fernet, InvalidToken
from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from ..config import allowed_file, Config

def _get_fernet() -> Fernet:
    # NOTE: For real production you must use a strong key and keep it secret.
    key = Config.ENCRYPTION_KEY
    # Ensure 32 url-safe base64-encoded bytes. Here for demo, we derive from provided string.
    base = key.encode("utf-8")
    base = (base * 2)[:32]
    import base64 as b64
    return Fernet(b64.urlsafe_b64encode(base))

def save_encrypted_file(file_storage: FileStorage, version_suffix: str = "") -> Tuple[str, str]:
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

    data = file_storage.read()
    f = _get_fernet()
    encrypted = f.encrypt(data)
    with open(stored_path, "wb") as f_out:
        f_out.write(encrypted)

    return stored_path, stored_name

def decrypt_file(filepath: str) -> bytes:
    with open(filepath, "rb") as f_in:
        encrypted = f_in.read()
    f = _get_fernet()
    try:
        return f.decrypt(encrypted)
    except InvalidToken:
        # In demo we just return raw data
        return encrypted
