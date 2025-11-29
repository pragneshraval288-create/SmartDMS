from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from backend.extensions import db, limiter, login_manager
from backend.models.models import User
from backend.forms.auth_forms import LoginForm, RegisterForm, ResetPasswordForm
from itsdangerous import URLSafeTimedSerializer

bp = Blueprint('auth', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

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
        hashed = generate_password_hash(form.password.data)
        user = User(username=username, password=hashed, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET','POST'])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/reset-password', methods=['GET','POST'])
@limiter.exempt
def reset_password():
    # simplistic reset: verifies username and allows password change
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('User not found', 'danger')
        else:
            user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password reset successfully!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)
