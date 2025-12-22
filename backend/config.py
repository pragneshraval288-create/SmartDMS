import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


class Config:
    # -------------------------------------------------
    # SECURITY  ✅ CRITICAL FIX
    # -------------------------------------------------
    SECRET_KEY = os.urandom(32)   # 🔥 NEW KEY ON EVERY SERVER START

    # -------------------------------------------------
    # DATABASE (MySQL)
    # -------------------------------------------------
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://smartdms_user:smartdms_pass@127.0.0.1:3306/smartdms_enterprise"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------------
    # FILE STORAGE
    # -------------------------------------------------
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "storage", "files")
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "pdf", "doc", "docx", "xls", "xlsx",
        "ppt", "pptx", "txt",
        "png", "jpg", "jpeg",
        "zip"
    }

    # -------------------------------------------------
    # ENCRYPTION
    # -------------------------------------------------
    ENCRYPTION_KEY = os.environ.get(
        "SMARTDMS_ENC_KEY",
        "dev-only-key-change-me-32b!!"
    )

    # -------------------------------------------------
    # FEATURES
    # -------------------------------------------------
    ENABLE_NOTIFICATIONS = True
    ENABLE_WORKFLOW = True

    # -------------------------------------------------
    # SESSION / AUTH ✅ FINAL
    # -------------------------------------------------
    SESSION_PERMANENT = False

    REMEMBER_COOKIE_DURATION = timedelta(seconds=0)
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    SESSION_REFRESH_EACH_REQUEST = False



# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def allowed_file(filename: str) -> bool:
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )
