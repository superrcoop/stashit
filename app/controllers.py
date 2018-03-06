import os
from flask import flash , request, url_for
from models import User
try:
    from urllib.parse import urlparse, urljoin
except ImportError:
     from urlparse import urlparse, urljoin

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

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def checkPassword(password):
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