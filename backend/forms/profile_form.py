from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
    EqualTo,
    Regexp,
    ValidationError,
)
from flask_login import current_user

phone_regex = r'^\+?\d{10,15}$'


class ProfileForm(FlaskForm):
    # Basic info
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=150)],
    )

    full_name = StringField(
        "Full Name",
        validators=[Optional(), Length(min=2, max=150)],
    )

    email = StringField(
        "Email",
        validators=[Optional(), Email(), Length(max=150)],
    )

    mobile = StringField(
        "Mobile Number",
        validators=[Optional(), Regexp(phone_regex, message="Invalid mobile number")],
    )

    dob = DateField(
        "Date of Birth (YYYY-MM-DD)",
        format="%Y-%m-%d",
        validators=[Optional()],
    )

    # 🔐 Password change section (used in template)
    current_password = PasswordField(
        "Current Password",
        validators=[Optional()],
    )

    new_password = PasswordField(
        "New Password",
        validators=[Optional(), Length(min=8, max=150)],
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            Optional(),
            EqualTo("new_password", message="Passwords must match"),
        ],
    )

    role = SelectField(
        "Role",
        choices=[("user", "User"), ("admin", "Admin")],
        validators=[Optional()],
    )

    submit = SubmitField("Submit")

    # ---------- Custom validators (unique fields) ----------

    def validate_username(self, field):
        uname = (field.data or "").strip()
        if not uname:
            return
        existing = User.query.filter(User.username.ilike(uname)).first()
        if existing and existing.id != current_user.id:
            raise ValidationError("Username already exists.")

    def validate_email(self, field):
        if not field.data:
            return
        email_value = field.data.strip().lower()
        existing = User.query.filter_by(email=email_value).first()
        if existing and existing.id != current_user.id:
            raise ValidationError("Email already exists.")

    def validate_mobile(self, field):
        if not field.data:
            return
        mobile_value = field.data.strip()
        existing = User.query.filter_by(mobile=mobile_value).first()
        if existing and existing.id != current_user.id:
            raise ValidationError("Mobile number already exists.")


# Import yaha rakha hai taaki circular import na aaye
from backend.models.models import User
