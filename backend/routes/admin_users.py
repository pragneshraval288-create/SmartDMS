from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from backend.extensions import db
from backend.models.models import User
from backend.forms.auth_forms import RegisterForm  #  Use this for user creation
from backend.security_helpers import validate_password
from backend.utils.permissions import admin_required

bp = Blueprint("admin_users", __name__, url_prefix="/admin/users")


@bp.route("/", methods=["GET"])
@login_required
@admin_required
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template("admin_users.html", users=users)


@bp.route("/create", methods=["GET","POST"])
@login_required
@admin_required
def create_user():

    form = RegisterForm()  #  RegisterForm stable hai (isme username, role सब hai)

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = (form.email.data or "").strip().lower()
        mobile = (form.mobile.data or "").strip() or None
        role = form.role.data or "user"

        #  Unique validation
        if User.query.filter(User.username.ilike(username)).first():
            flash("Username already exists!", "danger")
            return render_template("admin_user_form.html", form=form, mode="create")

        if email and User.query.filter(User.email == email).first():
            flash("Email already registered!", "danger")
            return render_template("admin_user_form.html", form=form, mode="create")

        if mobile and User.query.filter(User.mobile == mobile).first():
            flash("Mobile number already exists!", "danger")
            return render_template("admin_user_form.html", form=form, mode="create")

        #  Password rule
        ok, msg = validate_password(form.password.data)
        if not ok:
            flash(msg,"danger")
            return render_template("admin_user_form.html", form=form, mode="create")

        #  Create new user
        user = User(
            username = username,
            full_name = form.full_name.data,
            email = email or None,
            mobile = mobile,
            dob = form.dob.data.strftime("%Y-%m-%d") if form.dob.data else None,
            password_hash = generate_password_hash(form.password.data),
            role = role,
            created_at = datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()


        flash(" User Created Successfully!", "success")
        return redirect(url_for("admin_users.list_users"))

    return render_template("admin_user_form.html", form=form, mode="create")
