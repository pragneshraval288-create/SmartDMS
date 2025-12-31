import os
import base64
import hashlib
from typing import Optional

# New Imports for CryptoJS compatibility
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Existing Imports
from cryptography.fernet import Fernet, InvalidToken
from flask import current_app


class EncryptionService:
    """
    Central encryption service for:
    - Critical text data (Fernet)
    - Files/Documents (Fernet)
    - Frontend Password Decryption (AES-CBC)
    """

    # ============================
    # 1. INTERNAL: GET CIPHER (Fernet)
    # ============================
    @staticmethod
    def _get_fernet_cipher():
        """
        Get Fernet cipher using secret key from config (For Server-Side Storage)
        """
        key = current_app.config.get("ENCRYPTION_KEY")

        if not key:
            raise RuntimeError("ENCRYPTION_KEY is not set in config")

        # Ensure bytes
        if isinstance(key, str):
            key = key.encode()

        return Fernet(key)

    # ============================
    # 2. FRONTEND PASSWORD DECRYPTION (NEW & CRITICAL)
    # ============================
    @staticmethod
    def decrypt_frontend_payload(encrypted_text: str) -> Optional[str]:
        """
        Decrypts passwords sent from Frontend (CryptoJS AES).
        Uses 'FRONTEND_SECRET_KEY' from Config.
        """
        secret_key = current_app.config.get("FRONTEND_SECRET_KEY", "fallback-dev-key")
        
        try:
            if not encrypted_text:
                return None
                
            # 1. Base64 Decode
            encrypted_bytes = base64.b64decode(encrypted_text)
            
            # 2. Check header
            if encrypted_bytes[:8] != b'Salted__':
                return None

            # 3. Extract Salt & Ciphertext
            salt = encrypted_bytes[8:16]
            ciphertext = encrypted_bytes[16:]
            
            # 4. Derive Key & IV (OpenSSL/MD5 compatible)
            d = d_i = b''
            while len(d) < 32 + 16: # 32 key + 16 IV
                d_i = hashlib.md5(d_i + secret_key.encode('utf-8') + salt).digest()
                d += d_i
            
            key = d[:32]
            iv = d[32:48]
            
            # 5. Decrypt
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(ciphertext)
            decrypted = unpad(decrypted_padded, AES.block_size)
            
            return decrypted.decode('utf-8')

        except Exception as e:
            # Production mein print avoid karein
            return None

    # ============================
    # 3. TEXT ENCRYPTION (DB Storage)
    # ============================
    @staticmethod
    def encrypt_text(plain_text):
        """ Encrypt sensitive text before storing in DB (Fernet) """
        if not plain_text:
            return plain_text

        cipher = EncryptionService._get_fernet_cipher()
        encrypted = cipher.encrypt(str(plain_text).encode())
        return encrypted.decode()

    @staticmethod
    def decrypt_text(value):
        """ Safe decryption for DB text """
        if not value:
            return value

        cipher = EncryptionService._get_fernet_cipher()

        try:
            return cipher.decrypt(value.encode()).decode()
        except (InvalidToken, ValueError):
            return value

    # ============================
    # 4. FILE ENCRYPTION (Storage)
    # ============================
    @staticmethod
    def encrypt_file(input_path: str, output_path: str):
        """ Encrypt a file and save encrypted version """
        cipher = EncryptionService._get_fernet_cipher()

        with open(input_path, "rb") as f:
            file_data = f.read()

        encrypted_data = cipher.encrypt(file_data)

        with open(output_path, "wb") as f:
            f.write(encrypted_data)

    @staticmethod
    def decrypt_file(input_path: str, output_path: str):
        """ Decrypt a file and save decrypted version """
        cipher = EncryptionService._get_fernet_cipher()

        with open(input_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

    @staticmethod
    def decrypt_file_bytes(input_path: str) -> bytes:
        """ Decrypt file and return bytes (for secure download) """
        cipher = EncryptionService._get_fernet_cipher()

        with open(input_path, "rb") as f:
            encrypted_data = f.read()

        return cipher.decrypt(encrypted_data)