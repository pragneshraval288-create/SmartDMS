import os
from datetime import timedelta
from cryptography.fernet import Fernet

# Calculate paths relative to this file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


class Config:
    # -------------------------------------------------
    # SECURITY
    # -------------------------------------------------
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-in-prod-!!"
    )

    # -------------------------------------------------
    # DATABASE (MySQL)
    # -------------------------------------------------
    DB_USER = os.environ.get("DB_USER", "smartdms_user")
    DB_PASS = os.environ.get("DB_PASS", "smartdms_pass")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_NAME = os.environ.get("DB_NAME", "smartdms_enterprise")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------------
    # FILE STORAGE
    # -------------------------------------------------
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "storage", "files")
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB

    ALLOWED_EXTENSIONS = {
        "pdf", "doc", "docx", "xls", "xlsx",
        "ppt", "pptx", "txt",
        "png", "jpg", "jpeg",
        "zip"
    }

    # -------------------------------------------------
    # ENCRYPTION (CRITICAL DATA)
    # -------------------------------------------------
    # MUST be a valid Fernet key (32 url-safe base64 bytes)
    

    _raw_key = os.environ.get("SMARTDMS_ENC_KEY")

    if not _raw_key:
        raise RuntimeError("SMARTDMS_ENC_KEY is missing in .env")

    ENCRYPTION_KEY = _raw_key.encode()

    # -------------------------------------------------
    # FEATURES
    # -------------------------------------------------
    ENABLE_NOTIFICATIONS = True
    ENABLE_WORKFLOW = True

    # -------------------------------------------------
    # SESSION / AUTH
    # -------------------------------------------------
    SESSION_PERMANENT = False

    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    SESSION_REFRESH_EACH_REQUEST = False


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def allowed_file(filename: str) -> bool:
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in Config.ALLOWED_EXTENSIONS
    )
