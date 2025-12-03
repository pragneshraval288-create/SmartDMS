from datetime import datetime
import os
from werkzeug.utils import secure_filename
import re

#  Allowed file extensions
ALLOWED_EXT = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

def safe_filename(filename):
    return secure_filename(filename)


#   FINAL PASSWORD VALIDATION RULE
# Format: Uppercase + lowercase letters + one special (@#$%^&*) + digits
# Example: Pragnesh@8849
def validate_password(password: str):
    """
    Allowed format:
    Uppercase letter + lowercase letters + one special (@#$%^&*) + digits
    Example: Pragnesh@8849
    """
    pattern = r'^[A-Z][a-z]+[@#$%^&*][0-9]+$'

    if re.match(pattern, password):
        return True, "Password is valid."

    return False, "Password must be like: Pragnesh@8849 (Uppercase + lowercase + @/#/$/%/^/&/* + numbers)"
