from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    TextAreaField,
    DateField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
    Optional,
)
from .models import User
import re


# ---------------------------
# PASSWORD STRENGTH VALIDATOR
# ---------------------------
def strong_password(form, field):
    password = field.data or ""

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if re.search(r"\s", password):
        raise ValidationError("Password must not contain spaces.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number.")

    if not re.search(r"[@$!%*?&]", password):
        raise ValidationError(
            "Password must contain at least one special character (@ $ ! % * ? &)."
        )


# ---------------------------
# LOGIN FORM
# ---------------------------
class LoginForm(FlaskForm):
    username_or_email = StringField(
        "Username or Email",
        validators=[DataRequired(), Length(min=3, max=120)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


# ---------------------------
# REGISTER FORM
# ---------------------------
class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=120)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), strong_password]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )

    role = SelectField(
        "Role",
        choices=[
            ("user", "User"),
            ("admin", "Admin"),
        ],
        validators=[DataRequired()],
        default="user",
    )

    submit = SubmitField("Register")

    # ---------------------------
    # CUSTOM VALIDATORS
    # ---------------------------
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already taken.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email is already registered.")


# ---------------------------
# COMMENT FORM
# ---------------------------
class CommentForm(FlaskForm):
    content = TextAreaField(
        "Comment",
        validators=[DataRequired(), Length(min=1, max=1000)]
    )
    submit = SubmitField("Add Comment")


# ---------------------------
# SHARE FORM
# ---------------------------
class ShareForm(FlaskForm):
    username_or_email = StringField(
        "Username or Email",
        validators=[DataRequired(), Length(min=3, max=120)]
    )
    can_edit = BooleanField("Can edit")
    submit = SubmitField("Share")


# ---------------------------
# DOCUMENT FILTER FORM
# ---------------------------
class DocumentFilterForm(FlaskForm):
    search = StringField("Search", validators=[Optional()])

    file_type = SelectField(
        "Type",
        choices=[
            ("", "All types"),
            ("pdf", "PDF"),
            ("doc", "DOC"),
            ("docx", "DOCX"),
            ("xls", "XLS"),
            ("xlsx", "XLSX"),
            ("ppt", "PPT"),
            ("pptx", "PPTX"),
            ("txt", "TXT"),
            ("png", "PNG"),
            ("jpg", "JPG"),
            ("jpeg", "JPEG"),
            ("zip", "ZIP"),
        ],
        validators=[Optional()],
    )

    status = SelectField(
        "Status",
        choices=[
            ("active", "Active"),
            ("archived", "Archived"),
        ],
        validators=[Optional()],
    )

    sort = SelectField(
        "Sort by",
        choices=[
            ("newest", "Newest first"),
            ("oldest", "Oldest first"),
            ("alpha", "Alphabetical"),
            ("downloads", "Most downloaded"),
        ],
        validators=[Optional()],
    )

    date_from = DateField(
        "From date",
        format="%Y-%m-%d",
        validators=[Optional()]
    )
    date_to = DateField(
        "To date",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    submit = SubmitField("Apply")


# ---------------------------
# UPLOAD FORM
# ---------------------------
class UploadForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=255)]
    )

    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=2000)]
    )

    tags = StringField(
        "Tags",
        validators=[Optional(), Length(max=255)]
    )

    expiry_date = DateField(
        "Expiry date",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    files = FileField(
        "Files",
        validators=[
            FileRequired(),
            FileAllowed(
                [
                    "pdf", "doc", "docx",
                    "xls", "xlsx",
                    "ppt", "pptx",
                    "txt",
                    "png", "jpg", "jpeg",
                    "zip",
                ],
                "Invalid file type."
            )
        ]
    )

    submit = SubmitField("Upload")
