from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from ..extensions import db, csrf
from ..models import User, ActivityLog
from ..forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ==========================================
# 🔐 CRYPTOJS COMPATIBLE DECRYPTION LOGIC
# ==========================================

def get_key_and_iv(password, salt, key_length=32, iv_length=16):
    """
    Derives Key and IV from password and salt using OpenSSL's EVP_BytesToKey logic (MD5).
    This matches CryptoJS.AES.encrypt("msg", "pass") default behavior.
    """
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def decrypt_cryptojs_aes(encrypted_text, secret_key):
    """
    Decrypts a string encrypted by CryptoJS on the frontend.
    Format: "Salted__" + 8 bytes Salt + Ciphertext
    """
    try:
        # 1. Base64 Decode
        encrypted_bytes = base64.b64decode(encrypted_text)
        
        # 2. Check for "Salted__" header (Magic bytes)
        if encrypted_bytes[:8] != b'Salted__':
            # Agar 'Salted__' nahi mila, iska matlab shayad plain text hai
            return None

        # 3. Extract Salt & Ciphertext
        salt = encrypted_bytes[8:16]
        ciphertext = encrypted_bytes[16:]
        
        # 4. Derive Key & IV (Must match CryptoJS default MD5 logic)
        key, iv = get_key_and_iv(secret_key.encode('utf-8'), salt)
        
        # 5. Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        
        # 6. Unpad (Remove extra bytes added for block alignment)
        decrypted = unpad(decrypted_padded, AES.block_size)
        
        return decrypted.decode('utf-8')

    except Exception as e:
        print(f"⚠️ Decryption Failed: {e}")
        return None

# Secret Key (Must match Frontend JS variable)
SERVER_SECRET_KEY = "MY_SECRET_KEY_123"


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()

    if form.validate_on_submit():
        # --- DECRYPTION START ---
        raw_password = form.password.data
        decrypted_password = decrypt_cryptojs_aes(raw_password, SERVER_SECRET_KEY)
        
        # Fallback: Agar decryption fail hua (ya null aaya), toh raw value use karein
        final_password = decrypted_password if decrypted_password else raw_password
        # --- DECRYPTION END ---

        user = User.query.filter(
            or_(
                User.username == form.username_or_email.data,
                User.email == form.username_or_email.data
            )
        ).first()

        if user and user.check_password(final_password):
            # Check for approval
            if user.role != "admin" and (not user.is_active or not user.is_approved):
                flash("Your account is pending admin approval.", "warning")
                return render_template("auth/login.html", form=form)

            login_user(user, remember=form.remember.data)

            # Log Activity
            db.session.add(ActivityLog(
                action="login",
                user_id=user.id,
                ip_address=request.remote_addr
            ))
            db.session.commit()

            flash("Login successful.", "success")
            return redirect(url_for("dashboard.index"))

        flash("Invalid username/email or password.", "danger")

    return render_template("auth/login.html", form=form)


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated and not current_user.is_admin:
        flash("You are already logged in.", "info")
        return redirect(url_for("dashboard.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        if form.role.data == "admin":
            is_active = True
            is_approved = True
            action = "register_admin"
        else:
            is_active = False
            is_approved = False
            action = "register_pending_approval"

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            is_active=is_active,
            is_approved=is_approved
        )

        # --- DECRYPTION START ---
        # Registration form pe bhi JS encryption laga hona chahiye
        raw_password = form.password.data
        decrypted_password = decrypt_cryptojs_aes(raw_password, SERVER_SECRET_KEY)
        final_password = decrypted_password if decrypted_password else raw_password
        # --- DECRYPTION END ---

        user.set_password(final_password)

        db.session.add(user)
        db.session.commit()

        db.session.add(ActivityLog(
            action=action,
            user_id=user.id,
            ip_address=request.remote_addr
        ))
        db.session.commit()

        logout_user()

        flash(
            "Registration successful. Login after admin approval."
            if not is_approved else
            "Admin account created successfully.",
            "info"
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


# =========================
# FORGOT PASSWORD
# =========================
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
@csrf.exempt
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()

        if not identifier:
            flash("Please enter username or email.", "danger")
            return redirect(request.url)

        user = User.query.filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

        if not user:
            flash("No user found with this username/email.", "danger")
            return redirect(request.url)

        # Real app mein email bhejna chahiye, yahan direct reset page par bhej rahe hain
        return redirect(
            url_for("auth.reset_password", user_id=user.id)
        )

    return render_template("auth/forgot_password.html")


# =========================
# RESET PASSWORD
# =========================
@auth_bp.route("/reset-password/<int:user_id>", methods=["GET", "POST"])
@csrf.exempt
def reset_password(user_id):
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        # Form fields usually behave like standard inputs unless WTForms is used
        raw_new_password = request.form.get("password", "").strip()
        raw_confirm = request.form.get("confirm_password", "").strip()

        if not raw_new_password or not raw_confirm:
            flash("All fields are required.", "danger")
            return redirect(request.url)

        # --- DECRYPTION START ---
        # Note: Confirm password logic frontend par check honi chahiye encrypted string compare karke
        # Yahan hume decrypted values compare karni hongi
        
        dec_new = decrypt_cryptojs_aes(raw_new_password, SERVER_SECRET_KEY)
        final_new = dec_new if dec_new else raw_new_password

        dec_confirm = decrypt_cryptojs_aes(raw_confirm, SERVER_SECRET_KEY)
        final_confirm = dec_confirm if dec_confirm else raw_confirm
        # --- DECRYPTION END ---

        if final_new != final_confirm:
            flash("Passwords do not match.", "danger")
            return redirect(request.url)

        user.set_password(final_new)
        db.session.commit()

        db.session.add(ActivityLog(
            action="password_reset",
            user_id=user.id,
            ip_address=request.remote_addr
        ))
        db.session.commit()

        flash("Password reset successful. You can login now.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", user=user)


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
@login_required
def logout():
    db.session.add(ActivityLog(
        action="logout",
        user_id=current_user.id,
        ip_address=request.remote_addr
    ))
    db.session.commit()

    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))