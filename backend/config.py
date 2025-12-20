import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


class Config:
    # -------------------------------------------------
    # SECURITY
    # -------------------------------------------------
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-smartdms-enterprise"
    )

    # -------------------------------------------------
    # DATABASE (MySQL via PyMySQL)
    # -------------------------------------------------
    # Example:
    # mysql+pymysql://username:password@localhost:3306/smartdms_enterprise
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://smartdms_user:smartdms_pass@127.0.0.1:3306/smartdms_enterprise"
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
    # FILE ENCRYPTION (demo-level)
    # -------------------------------------------------
    ENCRYPTION_KEY = os.environ.get(
        "SMARTDMS_ENC_KEY",
        "dev-only-key-change-me-32b!!"
    )

    # -------------------------------------------------
    # FEATURE FLAGS
    # -------------------------------------------------
    ENABLE_NOTIFICATIONS = True
    ENABLE_WORKFLOW = True

    # -------------------------------------------------
    # SESSION / AUTH
    # -------------------------------------------------
    REMEMBER_COOKIE_DURATION = timedelta(days=7)


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def allowed_file(filename: str) -> bool:
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )
