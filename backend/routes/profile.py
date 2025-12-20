import os
import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user

from ..extensions import db
from ..models import User, ActivityLog

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


# ======================================================
# VIEW OWN PROFILE
# ======================================================
@profile_bp.route("/")
@login_required
def view_profile():
    return render_template(
        "profile/view.html",
        user=current_user
    )


# ======================================================
# EDIT OWN PROFILE (FULL FEATURE)
# ======================================================
@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()

        old_password = request.form.get("old_password", "").strip()
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        profile_image = request.files.get("profile_image")

        # -------------------------
        # BASIC VALIDATION
        # -------------------------
        if not email:
            flash("Email is required.", "danger")
            return redirect(url_for("profile.edit_profile"))

        # email uniqueness check
        existing = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if existing:
            flash("Email is already in use by another account.", "danger")
            return redirect(url_for("profile.edit_profile"))

        # -------------------------
        # UPDATE BASIC INFO
        # -------------------------
        current_user.email = email

        if hasattr(current_user, "full_name"):
            current_user.full_name = full_name

        # -------------------------
        # PROFILE IMAGE UPLOAD
        # -------------------------
        if profile_image and profile_image.filename:

            ext = os.path.splitext(profile_image.filename)[1].lower()

            if ext not in (".jpg", ".jpeg", ".png"):
                flash("Only JPG and PNG images are allowed.", "danger")
                return redirect(url_for("profile.edit_profile"))

            upload_dir = os.path.join(
                current_app.static_folder,
                "uploads",
                "profile"
            )
            os.makedirs(upload_dir, exist_ok=True)

            # delete old image (if exists)
            if current_user.profile_image:
                old_path = os.path.join(upload_dir, current_user.profile_image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            # save new image
            filename = f"{uuid.uuid4().hex}{ext}"
            save_path = os.path.join(upload_dir, filename)
            profile_image.save(save_path)

            current_user.profile_image = filename

        # -------------------------
        # PASSWORD CHANGE (OPTIONAL)
        # -------------------------
        if new_password or confirm_password or old_password:

            if not old_password:
                flash("Old password is required to change password.", "danger")
                return redirect(url_for("profile.edit_profile"))

            if not current_user.check_password(old_password):
                flash("Old password is incorrect.", "danger")
                return redirect(url_for("profile.edit_profile"))

            if not new_password or not confirm_password:
                flash("New password and confirm password are required.", "danger")
                return redirect(url_for("profile.edit_profile"))

            if new_password != confirm_password:
                flash("New password and confirm password do not match.", "danger")
                return redirect(url_for("profile.edit_profile"))

            current_user.set_password(new_password)

        # -------------------------
        # SAVE + LOG
        # -------------------------
        db.session.add(
            ActivityLog(
                action="profile_updated",
                user_id=current_user.id,
                ip_address=request.remote_addr
            )
        )

        db.session.commit()

        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.view_profile"))

    return render_template(
        "profile/edit.html",
        user=current_user
    )
