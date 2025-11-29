import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend.extensions import db, limiter, login_manager
from backend.models.models import User
from backend.forms.auth_forms import LoginForm, RegisterForm, ResetPasswordForm

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# ✅ LOGIN — Fixed redirect based on role + notifications login ke baad hi show hongi
@bp.route('/login', methods=['GET','POST'])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            flash('Logged in successfully!', 'success')  # flash carried रहेगा
            login_user(user, remember=form.remember.data if hasattr(form, 'remember') else True)

            # ✅ FIX: Redirect according to role (Admin = admin dashboard, User = normal home)
            if user.role == "admin":
                return redirect(url_for("documents.list"))  # admin ke liye best stable landing
            else:
                return redirect(url_for("dashboard.home"))  # normal user landing

        # ❌ Wrong credentials → stay on same page to show error AFTER login page (reload)
        flash('Invalid credentials', 'danger')
        return redirect(url_for('auth.login'))

    # First load (GET) → koi flash show nahi hogi (kyunki hum login page me flash remove करेंगे)
    return render_template('login.html', form=form)

# ✅ REGISTER — Already ok, role save stable
@bp.route('/register', methods=['GET','POST'])
@limiter.limit("5 per minute")
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        selected_role = form.role.data or "user"

        # Unique data checks
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists", "danger")
            return render_template("register.html", form=form)

        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already exists", "danger")
            return render_template("register.html", form=form)

        user = User(
            username=form.username.data,
            full_name=form.full_name.data,
            email=form.email.data.lower(),
            mobile=form.mobile.data or None,
            dob=str(form.dob.data) if form.dob.data else None,
            password_hash=generate_password_hash(form.password.data),  # ✅ Correct column
            role=selected_role
        )

        db.session.add(user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

# ✅ LOGOUT — unchanged stable
@bp.route('/logout')
@login_required
def logout():
    flash("Logged out!", "info")
    logout_user()
    return redirect(url_for('auth.login'))

# ✅ RESET PASSWORD — unchanged stable
@bp.route('/reset-password', methods=['GET','POST'])
@limiter.limit("5 per minute")
def reset_password():
    form = ResetPasswordForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            flash("User not found", "danger")
            return render_template("reset_password.html", form=form)

        if user.email != form.email.data.lower():
            flash("Email not match", "danger")
            return render_template("reset_password.html", form=form)

        if user.mobile != form.mobile.data:
            flash("Mobile not match", "danger")
            return render_template("reset_password.html", form=form)

        user.password_hash = generate_password_hash(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash("Password reset successful!", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)
