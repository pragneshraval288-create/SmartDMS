from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required!', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrap

def user_or_admin_owns(doc):
    return (current_user.role == 'admin') or (current_user.id == doc.uploader_id)
