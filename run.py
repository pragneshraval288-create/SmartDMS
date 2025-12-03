import pathlib
from backend.app import create_app
from backend.extensions import db, limiter

BASE_DIR = pathlib.Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"

def ensure_database():
    INSTANCE_DIR.mkdir(exist_ok=True, parents=True)
    db_file = INSTANCE_DIR / "smartdms.db"
    if not db_file.exists():
        db_file.write_text("")

def ensure_upload_dirs():
    (INSTANCE_DIR / "uploads" / "profile_pics").mkdir(exist_ok=True, parents=True)
    (INSTANCE_DIR / "uploads").mkdir(exist_ok=True, parents=True)

def main():
    ensure_database()
    ensure_upload_dirs()

    app = create_app()

    with app.app_context():
        db.create_all()

    # Limiter storage explicit declare kar diya → warning bhi production-ready path ke sath
    limiter.storage_uri = "memory://"   

    #  Sirf ek baar print karo
    print("\n Server started! Open browser → http://127.0.0.1:5000/\n")

    app.run(debug=False, host="127.0.0.1", port=5000)  # debug off = clean startup

if __name__ == "__main__":
    main()
