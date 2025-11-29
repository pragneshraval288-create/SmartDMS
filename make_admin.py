from backend.app import create_app
from backend.models.models import User  # ✅ also ensure User is imported
from backend.extensions import db

app = create_app()

with app.app_context():
    email = "admin@gmail.com"  # 👈 yaha apna admin email daalna
    u = User.query.filter_by(email=email).first()

    if not u:
        print(f"❌ User with email {email} NOT FOUND in database!")
        print("➡️ Pehle website se us email se account register karo, fir script run karna.")
    else:
        u.role = "admin"
        db.session.commit()
        print(f"✅ {email} is now ADMIN 🎀")
