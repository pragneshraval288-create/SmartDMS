import os, secrets
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXT = {"pdf","docx","xlsx","pptx","txt","jpg","jpeg","png"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[-1].lower() in ALLOWED_EXT

def save_file(file):
    name, ext = secure_filename(file.filename).rsplit('.',1)
    version = 1
    final_name = f"{name}_v{version}.{ext}"
    save_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(save_dir, exist_ok=True)
    file.save(os.path.join(save_dir, final_name))
    return final_name
