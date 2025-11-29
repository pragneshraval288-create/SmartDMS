from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from backend.extensions import db, limiter, login_manager
from backend.models.models import User
from backend.forms.auth_forms import LoginForm, RegisterForm, ResetPasswordForm
from backend.security_helpers import validate_password
from itsdangerous import URLSafeTimedSerializer
from urllib.parse import urlparse
from datetime import timedelta, datetime

bp = Blueprint('auth', __name__, template_folder='templates')

login_manager.login_view = "auth.login"
login_manager.login_message = None
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# ✅ REGISTER ROUTE
@bp.route('/register', methods=['GET','POST'])
@limiter.limit("10 per hour")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Username already exists', 'danger')
            return render_template('register.html', form=form)

        # ✅ Password validation
        ok, msg = validate_password(form.password.data)
        if not ok:
            flash(msg, 'danger')
            return render_template('register.html', form=form)

        hashed = generate_password_hash(form.password.data)
        user = User(username=username, password=hashed, role=form.role.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')

        return redirect(url_for("auth.login"))

    return render_template('register.html', form=form)


# ✅ LOGIN ROUTE
@bp.route('/login', methods=['GET','POST'])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')

            # ✅ Handle `next=` param securely
            next_url = request.args.get("next")
            if next_url:
                parsed = urlparse(next_url)
                if parsed.netloc == "" and not parsed.path.startswith("/register"):
                    return redirect(next_url)

            # ✅ Finally redirect to Dashboard
            return redirect(url_for("dashboard.home"))

        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for("auth.login"))

    return render_template('login.html', form=form)


# ✅ LOGOUT ROUTE ✔
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for("auth.login"))


# ✅ RESET PASSWORD ROUTE ✔
@bp.route('/reset-password', methods=['GET','POST'])
@limiter.exempt
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for("auth.login"))

        ok, msg = validate_password(form.new_password.data)
        if not ok:
            flash(msg, 'danger')
            return render_template("reset_password.html", form=form)

        user.password = generate_password_hash(form.new_password.data)
        db.session.commit()

        flash('Password reset successfully!', 'success')
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)


# ✅ UNAUTHORIZED HANDLER (fixed — Register/other page me leak नहीं होगा)
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please log in to access this page.", "warning")

    next_url = request.args.get("next")
    if next_url:
        parsed = urlparse(next_url)
        if parsed.netloc == "" and not parsed.path.startswith("/register"):
            return redirect(next_url)

    return redirect(url_for("auth.login"))
