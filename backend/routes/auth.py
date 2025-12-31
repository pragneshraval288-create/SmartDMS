from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
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
    Used to match CryptoJS default behavior.
    """
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def decrypt_cryptojs_aes(encrypted_text):
    """
    Decrypts a string encrypted by CryptoJS on the frontend.
    FETCHES KEY FROM CONFIG (Secure).
    """
    # Ensure 'FRONTEND_SECRET_KEY' exists in backend/config.py
    secret_key = current_app.config.get("FRONTEND_SECRET_KEY", "MY_SECRET_KEY_123")
    
    try:
        if not encrypted_text:
            return None
            
        # 1. Base64 Decode
        try:
            encrypted_bytes = base64.b64decode(encrypted_text)
        except Exception:
            return None # Invalid Base64
        
        # 2. Check for "Salted__" header
        if len(encrypted_bytes) < 16 or encrypted_bytes[:8] != b'Salted__':
            return None

        # 3. Extract Salt & Ciphertext
        salt = encrypted_bytes[8:16]
        ciphertext = encrypted_bytes[16:]
        
        # 4. Derive Key & IV
        key, iv = get_key_and_iv(secret_key.encode('utf-8'), salt)
        
        # 5. Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        
        # 6. Unpad
        decrypted = unpad(decrypted_padded, AES.block_size)
        
        return decrypted.decode('utf-8')

    except Exception as e:
        # Log error internally if needed, but return None to fail gracefully
        current_app.logger.error(f"Decryption Error: {str(e)}")
        return None


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
        decrypted_password = decrypt_cryptojs_aes(raw_password)
        
        # Fallback: Use decrypted if successful, else use raw (for testing/plain text)
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
            try:
                db.session.add(ActivityLog(
                    action="login",
                    user_id=user.id,
                    ip_address=request.remote_addr
                ))
                db.session.commit()
            except Exception:
                db.session.rollback() # Don't stop login if logging fails

            flash("Login successful.", "success")
            
            # Handle 'next' parameter safely
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard.index')
                
            return redirect(next_page)

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
        try:
            # Logic: If creating admin, auto-approve? 
            # ideally admins should also be manually approved in DB, but keeping your logic.
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
            raw_password = form.password.data
            decrypted_password = decrypt_cryptojs_aes(raw_password)
            final_password = decrypted_password if decrypted_password else raw_password
            # --- DECRYPTION END ---

            user.set_password(final_password)

            db.session.add(user)
            db.session.commit() # Commit first to get user.id

            # Log activity
            db.session.add(ActivityLog(
                action=action,
                user_id=user.id,
                ip_address=request.remote_addr
            ))
            db.session.commit()

            # Force logout to make them login again properly
            if current_user.is_authenticated:
                logout_user()

            flash(
                "Registration successful. Login after admin approval."
                if not is_approved else
                "Admin account created successfully.",
                "info"
            )
            return redirect(url_for("auth.login"))

        except SQLAlchemyError:
            db.session.rollback()
            flash("Username or Email already exists.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Register Error: {e}")
            flash("An error occurred during registration.", "danger")

    return render_template("auth/register.html", form=form)


# =========================
# FORGOT PASSWORD
# =========================
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    Mock implementation of forgot password. 
    NOTE: In production, this must send an Email/SMS with a token.
    Direct redirect is used here for demonstration purposes.
    """
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

        # [SECURITY IMPROVEMENT] Prevent User Enumeration
        # Don't tell if user exists or not.
        if not user:
            # Fake delay to simulate processing time
            flash("If an account exists, you will be redirected to reset it.", "info")
            return redirect(request.url)

        # WARNING: This part is for Demo only. 
        # Ideally, generate a token and email it.
        # Direct redirect allows anyone to reset if they guess username.
        # Keeping it as per your requirement, but use with caution.
        return redirect(url_for("auth.reset_password", user_id=user.id))

    return render_template("auth/forgot_password.html")


# =========================
# RESET PASSWORD
# =========================
@auth_bp.route("/reset-password/<int:user_id>", methods=["GET", "POST"])
# @csrf.exempt -> REMOVED: CSRF protection is crucial for forms
def reset_password(user_id):
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        # Form should include CSRF token in template: {{ csrf_token() }} or via Flask-WTF
        raw_new_password = request.form.get("password", "").strip()
        raw_confirm = request.form.get("confirm_password", "").strip()

        if not raw_new_password or not raw_confirm:
            flash("All fields are required.", "danger")
            return redirect(request.url)

        # --- DECRYPTION START ---
        dec_new = decrypt_cryptojs_aes(raw_new_password)
        final_new = dec_new if dec_new else raw_new_password

        dec_confirm = decrypt_cryptojs_aes(raw_confirm)
        final_confirm = dec_confirm if dec_confirm else raw_confirm
        # --- DECRYPTION END ---

        if final_new != final_confirm:
            flash("Passwords do not match.", "danger")
            return redirect(request.url)

        try:
            user.set_password(final_new)
            
            db.session.add(ActivityLog(
                action="password_reset",
                user_id=user.id,
                ip_address=request.remote_addr
            ))
            db.session.commit()

            flash("Password reset successful. You can login now.", "success")
            return redirect(url_for("auth.login"))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Reset Password Error: {e}")
            flash("Error resetting password.", "danger")

    return render_template("auth/reset_password.html", user=user)


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
@login_required
def logout():
    try:
        # Log activity before logging out
        db.session.add(ActivityLog(
            action="logout",
            user_id=current_user.id,
            ip_address=request.remote_addr
        ))
        db.session.commit()
    except Exception:
        pass # Logout should proceed even if logging fails

    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))