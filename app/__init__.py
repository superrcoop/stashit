from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_mail import Mail
import os , psycopg2
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(__name__)# Flask-Login login manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"

UPLOAD_FOLDER = './app/static/uploads'


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
#Using default bcrypt settings
#app.config['BCRYPT_LOG_ROUNDS'] 				= 12
#app.config['BCRYPT_HASH_IDENT'] 				= '2b'
#app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] 	= False

DATABASE_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] 	= True
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

db = SQLAlchemy(app)
mail = Mail(app)
from app import views