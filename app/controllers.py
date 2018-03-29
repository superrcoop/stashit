import os 
from flask import flash , request, url_for
from .models import User
from .forms import ALLOWED_EXTENSIONS
from re import compile
EMAIL_REGEX = compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
PASSWORD_REGEX = compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})')
ALPHA_REGEX = compile(r'^[A-Za-z]+(?:[. \'-][A-Za-z]+)*$')
USERNAME_REGEX = compile(r'^[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)*$')
URL_REGEX=compile(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$')

def get_uploaded_images(user_URI):
    rootdir = os.getcwd()
    for subdir,dirs,files in os.walk(rootdir +user_URI[1:-1]):
        for file in files:
            ls=os.path.join(subdir,file).split('/')[-2:]
    return '/'.join(ls)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def regexPassword(password): 
    if not PASSWORD_REGEX.match(password): 
        return False
    return True

def regexAlpha(alpha):
    if not ALPHA_REGEX.match(alpha):
        return False
    return True

def regexEmail(email):
    if not EMAIL_REGEX.match(email):
        return False
    return True

def regexUsername(username):
    if not USERNAME_REGEX.match(username):
        return False
    return True

def regexURL(URL):
    if not URL_REGEX.match(URL):
        return False
    return True
    
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc