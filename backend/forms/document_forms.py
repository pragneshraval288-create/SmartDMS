from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Optional, Length, ValidationError

ALLOWED_EXT = {"pdf", "docx", "xlsx", "pptx", "txt", "png", "jpg", "jpeg"}

class DocumentForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Title is required ❗"),
        Length(max=200)
    ])
    tags = StringField('Tags', validators=[
        Optional(),
        Length(max=200)
    ])

    file = FileField('File', validators=[Optional()])

    submit = SubmitField('Submit')

    # ✅ Stable file validation implemented
    def validate_file(self, field):
        if field.data:
            filename = field.data.filename
            ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
            if ext not in ALLOWED_EXT:
                raise ValidationError("File type not supported ❗")
