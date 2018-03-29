import uuid , datetime , random , os ,errno
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from bcrypt import hashpw, gensalt
from . import db ,UPLOAD_FOLDER

def generate_id():
    return int(str(uuid.uuid4().int)[:8])

def generate_rcode():
    return int(str(uuid.uuid4().int)[:6])

def get_date():
    return datetime.datetime.now().today()

def generate_file_URI():
    URI=UPLOAD_FOLDER+'/'+str(uuid.uuid4().get_hex()[0:12])+'/'
    if not os.path.exists(URI):
        try:
            os.makedirs(URI)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    return URI

class User(db.Model, UserMixin):
	__tablename__ 	= 'userstable'
	id 				= db.Column(db.Integer, primary_key=True)
	username 		= db.Column(db.String(80), unique=True)
	email 			= db.Column(db.String(80), unique=True,nullable=False)
	first_name 		= db.Column(db.String(80))
	last_name 		= db.Column(db.String(80))
	_password		= db.Column(db.String(255),nullable=False)
	recoveryCode 	= db.Column(db.Integer,nullable=False)
	authenticated   = db.Column(db.Boolean,default=False,nullable=False)
	date_joined		= db.Column(db.Date,nullable=False)
	file_URI 		= db.Column(db.String(80),nullable=False)


	def __init__(self, username, first_name, last_name, email, plain_password, id=None):
		if id: 
			self.id 		= id
		else:
			self.id 		= generate_id()
		self.username 		= username
		self.email 			= email
		self.password 		= plain_password
		self.first_name 	= first_name 
		self.last_name 		= last_name
		self.recoveryCode 	= generate_rcode()
		self.authenticated  = False
		self.date_joined    = get_date()
		self.file_URI       = generate_file_URI()

	def setRecoveryCode(self):
		self.recoveryCode = generate_rcode()

	def checkCode(self, code):
		if code == self.recoveryCode:
			self.setRecoveryCode
			self.authenticated=True
			return True
		return False

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def password(self,plain_password):
		self._password = hashpw(plain_password,gensalt())
 
	@hybrid_method
	def is_correct_password(self, plain_password):
		return hashpw(plain_password,self.password)==self.password
	
	def get_id(self):
		try:
			return unicode(self.id)  # python 2 support
		except NameError:
			return str(self.id)  # python 3 support

	def is_authenticated(self):
		if self.authenticated:
			return True
		return False

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def __repr__(self):
		return '<User %r>' % (self.username)
