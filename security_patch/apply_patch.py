
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
print('Project root:', ROOT)
# Paths
app_py = ROOT / 'backend' / 'app.py'
auth_py = ROOT / 'backend' / 'routes' / 'auth.py'
helpers_py = ROOT / 'backend' / 'security_helpers.py'
secure_auth_src = ROOT / 'security_patch' / 'secure_auth.py'

def replace_placeholder(path, replacement, marker='...'):
    text = path.read_text()
    if marker in text:
        new = text.replace(marker, replacement)
        path.write_text(new)
        print('Replaced placeholder in', path)
        return True
    else:
        print('No placeholder "{}" in {}'.format(marker, path))
        return False

replacement = secure_auth_src.read_text()
replaced = replace_placeholder(auth_py, replacement)
if not replaced:
    dest = ROOT / 'backend' / 'routes' / 'secure_auth.py'
    dest.write_text(replacement)
    print('Created', dest)

helpers_content = '''import os
from werkzeug.utils import secure_filename

ALLOWED_EXT = {'pdf','docx','txt','png','jpg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

def safe_filename(filename):
    return secure_filename(filename)
'''
helpers_py.write_text(helpers_content)
print('Created security_helpers at', helpers_py)
print('Patching complete. Review changes and run your app.')
