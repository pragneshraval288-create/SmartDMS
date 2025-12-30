import os
from cryptography.fernet import Fernet, InvalidToken
from flask import current_app


class EncryptionService:
    """
    Central encryption service for:
    - Critical text data
    - Files (documents)
    Handles both encrypted and legacy (plain) data safely.
    """

    # ============================
    # INTERNAL: GET CIPHER
    # ============================
    @staticmethod
    def _get_cipher():
        """
        Get Fernet cipher using secret key from config
        """
        key = current_app.config.get("ENCRYPTION_KEY")

        if not key:
            raise RuntimeError("ENCRYPTION_KEY is not set in config")

        # Ensure bytes
        if isinstance(key, str):
            key = key.encode()

        return Fernet(key)

    # ============================
    # TEXT ENCRYPTION
    # ============================

    @staticmethod
    def encrypt_text(plain_text):
        """
        Encrypt sensitive text before storing in DB
        """
        if not plain_text:
            return plain_text

        cipher = EncryptionService._get_cipher()
        encrypted = cipher.encrypt(str(plain_text).encode())
        return encrypted.decode()

    @staticmethod
    def decrypt_text(value):
        """
        Safe decryption:
        - If value is encrypted → decrypt
        - If value is plain / legacy → return as-is
        """
        if not value:
            return value

        cipher = EncryptionService._get_cipher()

        try:
            return cipher.decrypt(value.encode()).decode()
        except (InvalidToken, ValueError):
            # 🔥 IMPORTANT:
            # Old unencrypted data OR mismatched key
            return value

    # ============================
    # FILE ENCRYPTION
    # ============================

    @staticmethod
    def encrypt_file(input_path: str, output_path: str):
        """
        Encrypt a file and save encrypted version
        """
        cipher = EncryptionService._get_cipher()

        with open(input_path, "rb") as f:
            file_data = f.read()

        encrypted_data = cipher.encrypt(file_data)

        with open(output_path, "wb") as f:
            f.write(encrypted_data)

    @staticmethod
    def decrypt_file(input_path: str, output_path: str):
        """
        Decrypt a file and save decrypted version
        """
        cipher = EncryptionService._get_cipher()

        with open(input_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

    # ============================
    # STREAM DECRYPT (DOWNLOAD)
    # ============================

    @staticmethod
    def decrypt_file_bytes(input_path: str) -> bytes:
        """
        Decrypt file and return bytes (for secure download)
        """
        cipher = EncryptionService._get_cipher()

        with open(input_path, "rb") as f:
            encrypted_data = f.read()

        return cipher.decrypt(encrypted_data)
