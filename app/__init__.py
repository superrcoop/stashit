from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_mail import Mail
# Config Values
USERNAME = 'admin@admin.com'
PASSWORD = 'password123'

# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
UPLOAD_FOLDER = './app/static/uploads'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] 					= UPLOAD_FOLDER
app.config['RECAPTCHA_USE_SSL'] 				= True
app.config['RECAPTCHA_PUBLIC_KEY'] 				= '6LcVT0oUAAAAAHC2ThJf4cyndvFBb5blLhqhYxNE'
app.config['RECAPTCHA_PRIVATE_KEY'] 			= '6LcVT0oUAAAAAJ_b9ALcRLstq-2UfyxRnCf-To8x'
app.config['RECAPTCHA_OPTIONS'] 				= {'theme': 'white'}
app.config['SECRET_KEY'] 						= 'supercalifragilisticespialidocious'

app.config['MAIL_DEFAULT_SENDER']				= 'stashit.no.reply@gmail.com'
app.config['MAIL_SERVER']						= 'smtp.gmail.com'
app.config['MAIL_PORT'] 						= 465
app.config['MAIL_USERNAME'] 					= 'stashit.no.reply@gmail.com'
app.config['MAIL_PASSWORD'] 					= 'Stashitpassword'
app.config['MAIL_USE_TLS'] 						= False
app.config['MAIL_USE_SSL'] 						= True

app.config['SQLALCHEMY_DATABASE_URI'] 			= 'postgresql://postgres:password@localhost/securitydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] 	= True

db = SQLAlchemy(app)
mail = Mail(app)

from app import views