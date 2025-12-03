import os
import pathlib
import secrets
from datetime import timedelta  #  FIXED import added

BASE_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

TEMPLATE_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"
INSTANCE_DIR = PROJECT_ROOT / "instance"

IST_OFFSET = 19800  # 5 hours 30 minutes in seconds for app-wide timezone awareness

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{INSTANCE_DIR / 'smartdms.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "10")) * 1024 * 1024

    #  Upload folder inside instance
    UPLOAD_FOLDER = str(INSTANCE_DIR / "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    #  Remember cookie duration fixed & safe
    REMEMBER_COOKIE_DURATION = timedelta(
        days=int(os.environ.get("REMEMBER_COOKIE_DAYS", "1"))
    )

    #  Flash leak prevention stable
    LOGIN_DISABLED_FLASH = True  #  Flash message leak ko rokta hai

    #  Cookie security stable for local testing
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # Local test ke liye stable
