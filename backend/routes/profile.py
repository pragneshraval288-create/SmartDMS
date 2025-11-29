import os
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    abort,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from backend.extensions import db
from backend.models.models import User
from backend.forms.profile_form import ProfileForm

bp = Blueprint("profile", __name__, url_prefix="/profile")


# ---------- Helpers ----------

def _save_profile_pic(file, old_filename: str | None = None) -> str:
    """
    Profile picture ko static/profile_pics me save karta hai
    aur naya filename return karta hai.
    """
    if not file or not file.filename:
        return old_filename

    filename = secure_filename(file.filename)
    # unique name
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{int(datetime.utcnow().timestamp())}{ext}"

    upload_folder = os.path.join(current_app.static_folder, "profile_pics")
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, new_filename)
    file.save(file_path)

    # optionally: purani pic delete karni ho to yaha handle kar sakte ho
    return new_filename


def _get_target_user(user_id):
    """
    Admin dusre user ka profile view/edit kar sakta hai.
    Normal user sirf apna.
    """
    if user_id is None or current_user.role != "admin":
        return current_user

    target = User.query.get_or_404(user_id)
    return target


# ---------- Routes ----------


@bp.route("/", defaults={"user_id": None})
@bp.route("/<int:user_id>")
@login_required
def profile_view(user_id):
    target_user = _get_target_user(user_id)
    # view mode me form nahi bhej rahe
    return render_template("profile.html", user=target_user, form=None, edit_mode=False)


@bp.route("/edit", defaults={"user_id": None}, methods=["GET", "POST"])
@bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile_edit(user_id):
    target_user = _get_target_user(user_id)

    # Sirf admin hi kisi aur user ka role/username change kare
    if target_user.id != current_user.id and current_user.role != "admin":
        abort(403)

    form = ProfileForm(obj=target_user)

    # 🔹 FIX: agar DB me dob string hai to DateField ke liye date object me convert karo
    if request.method == "GET":
        if isinstance(target_user.dob, str) and target_user.dob:
            try:
                form.dob.data = datetime.strptime(target_user.dob, "%Y-%m-%d").date()
            except ValueError:
                form.dob.data = None

    if form.validate_on_submit():
        # ---- Basic fields update ----
        target_user.full_name = form.full_name.data or None
        target_user.email = (form.email.data or "").strip().lower() or None
        target_user.mobile = (form.mobile.data or "").strip() or None

        # 🔹 DOB ko DB me string ke roop me store kar rahe hain (safe for templates)
        if form.dob.data:
            target_user.dob = form.dob.data.strftime("%Y-%m-%d")
        else:
            target_user.dob = None

        # username / role sirf admin change kare
        if current_user.role == "admin":
            target_user.username = form.username.data.strip()
            if form.role.data:
                target_user.role = form.role.data

        # ---- Profile picture ----
        file = request.files.get("profile_pic")
        if file and file.filename:
            target_user.profile_pic = _save_profile_pic(
                file, old_filename=target_user.profile_pic
            )

        # ---- Password change (optional) ----
        if form.new_password.data:
            # 1. current password required
            if not form.current_password.data:
                form.current_password.errors.append("Please enter your current password.")
                return render_template(
                    "profile.html",
                    user=target_user,
                    form=form,
                    edit_mode=True,
                )

            # 2. Verify current password
            # NOTE: yaha `password_hash` assume kiya hai.
            # Agar tumhare model me column ka naam kuch aur hai
            # to niche dono jagah usko change kar dena.
            if not check_password_hash(
                target_user.password_hash, form.current_password.data
            ):
                form.current_password.errors.append("Current password is incorrect.")
                return render_template(
                    "profile.html",
                    user=target_user,
                    form=form,
                    edit_mode=True,
                )

            # 3. Set new password
            target_user.password_hash = generate_password_hash(form.new_password.data)

        db.session.commit()
        flash("Profile updated successfully.", "success")

        # Redirect back to view page
        return redirect(
            url_for(
                "profile.profile_view",
                user_id=target_user.id
                if (current_user.role == "admin" and target_user.id != current_user.id)
                else None,
            )
        )

    # GET request / or form errors
    return render_template("profile.html", user=target_user, form=form, edit_mode=True)
