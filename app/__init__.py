from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_mail import Mail
import os , psycopg2



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
#app.config['BCRYPT_LOG_ROUNDS'] 				= 6
#app.config['BCRYPT_HASH_IDENT'] 				= '2b'
#app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] 		= False

DATABASE_URL 									= os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] 	= True
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

db = SQLAlchemy(app)
mail = Mail(app)
from app import views