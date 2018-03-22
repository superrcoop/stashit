import os 
from flask import flash , request, url_for
from .models import User
from .forms import ALLOWED_EXTENSIONS
from re import compile
EMAIL_REGEX = compile(r"\"?([-a-zA-Z0-9._?{}]+@\w+\.\w+)\"?")
PASSWORD_REGEX = compile(r'^([\w!\-#@&%]{8,})$')
ALPHA_REGEX = compile(r'^([a-zA-z-\']{1,})$')

def get_uploaded_images():
    rootdir = os.getcwd()
    ls = []
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
            ls.append(os.path.join(subdir, file).split('/')[-1])
    return ls

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def flash_errors(form):
# Flash errors from the form if validation fails
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form,field).label.text,error),'danger')

def checkPassword(password): #SUGGESTION: check both password and conf_password to increase efficiency
    if not PASSWORD_REGEX.match(password): 
        return False
    return True

def checkAlpha(alpha):
    if not ALPHA_REGEX.match(alpha):
        return False
    return True

def checkEmail(email):
    if not EMAIL_REGEX.match(email):
        return False
    return True

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc