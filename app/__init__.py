from flask import Flask

# Config Values
USERNAME = 'admin@admin.com'
PASSWORD = 'password123'

# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER = './app/static/uploads'


app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECAPTCHA_USE_SSL'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcVT0oUAAAAAHC2ThJf4cyndvFBb5blLhqhYxNE'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcVT0oUAAAAAJ_b9ALcRLstq-2UfyxRnCf-To8x'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
from app import views