from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from ..extensions import db, csrf
from ..models import User, ActivityLog
from ..forms import LoginForm, RegisterForm

# 🔐 ADDED (for decrypt)
import base64

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")



# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()

    if form.validate_on_submit():

        # 🔐 ADDED: decrypt password coming from frontend
        encrypted_password = form.password.data
        try:
            decrypted_password = base64.b64decode(encrypted_password).decode()[::-1]
        except Exception:
            decrypted_password = encrypted_password

        user = User.query.filter(
            or_(
                User.username == form.username_or_email.data,
                User.email == form.username_or_email.data
            )
        ).first()

        # 🔐 CHANGED INPUT ONLY (logic untouched)
        if user and user.check_password(decrypted_password):

            # block non-approved users (except admin)
            if user.role != "admin" and (not user.is_active or not user.is_approved):
                flash("Your account is pending admin approval.", "warning")
                return render_template("auth/login.html", form=form)

            login_user(user, remember=form.remember.data)

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

        user.set_password(form.password.data)

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
# FORGOT PASSWORD (NO LOGIN)
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

        return redirect(
            url_for("auth.reset_password", user_id=user.id)
        )

    return render_template("auth/forgot_password.html")


# =========================
# RESET PASSWORD (NO LOGIN)
# =========================
@auth_bp.route("/reset-password/<int:user_id>", methods=["GET", "POST"])
@csrf.exempt
def reset_password(user_id):
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        new_password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()

        if not new_password or not confirm:
            flash("All fields are required.", "danger")
            return redirect(request.url)

        if new_password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(request.url)

        user.set_password(new_password)
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