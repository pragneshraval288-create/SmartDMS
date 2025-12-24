import os
from datetime import timedelta

# Calculate paths relative to this file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


class Config:
    # -------------------------------------------------
    # SECURITY
    # -------------------------------------------------
    # ⚠️ CRITICAL FIX: Do NOT use os.urandom(32) here.
    # If the app restarts, the key changes, and all users get logged out immediately.
    # Use a fixed string for dev, and an environment variable for prod.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod-!!")

    # -------------------------------------------------
    # DATABASE (MySQL)
    # -------------------------------------------------
    # Best Practice: Load credentials from environment variables
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
    # ENCRYPTION
    # -------------------------------------------------
    # Ensure this key is kept safe and NOT changed once files are encrypted
    ENCRYPTION_KEY = os.environ.get(
        "SMARTDMS_ENC_KEY",
        "dev-only-key-change-me-32b!!" # Ensure this string is handled correctly by your cipher
    )

    # -------------------------------------------------
    # FEATURES
    # -------------------------------------------------
    ENABLE_NOTIFICATIONS = True
    ENABLE_WORKFLOW = True

    # -------------------------------------------------
    # SESSION / AUTH
    # -------------------------------------------------
    # If False, session dies when browser closes.
    SESSION_PERMANENT = False 

    # ⚠️ LOGIC FIX: 'Remember Me' usually implies keeping the session alive for days.
    # Setting this to 0 seconds effectively disables "Remember Me".
    # Standard is 7 to 30 days.
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # These prevent the cookie from being refreshed on every single click (performance)
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    SESSION_REFRESH_EACH_REQUEST = False


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
# Ideally, move this to a 'utils.py' file to keep config pure, 
# but it works here for small apps.
def allowed_file(filename: str) -> bool:
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )