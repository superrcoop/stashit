from . import db
from time import time
from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash
class User(db.Model, UserMixin):
	__tablename__ 	= 'userstable'
	id 				= db.Column(db.Integer, primary_key=True)
	username 		= db.Column(db.String(80), unique=True)
	email 			= db.Column(db.String(80), unique=True)
	first_name 		= db.Column(db.String(80))
	last_name 		= db.Column(db.String(80))
	password		= db.Column(db.String(80))
	salt 			= db.Column(db.Integer)
	profile_photo 	= db.Column(db.String(80))

	def __init__(self, username, first_name, last_name, email, password, salt, id = None, profile_photo = 'default.png'):
		if id: 
			self.id 		= id
		else:
			self.id 		= long(time())
		self.username 		= username
		self.email 			= email
		self.password 		= generate_password_hash(password + str(salt), method = 'sha256')
		self.salt 			= salt
		self.first_name 	= first_name 
		self.last_name 		= last_name
		self.profile_photo 	= profile_photo

	def checkPassword(self, password):
		return check_password_hash(self.password, password+str(self.salt))


def users():
    user = User(id=0,username='administrator',first_name='Admin',last_name='User',email='admin@stashit.com',password='administrator',salt=random.randint(827,18273),profile_photo = 'default.png')
    db.session.add(user)
    user = User(username='milly_stash',first_name='Milton',last_name='Edwards',email='me@stashit.com',password='password123',salt=random.randint(827,18273),profile_photo = 'default.png')
    db.session.add(user)
    user = User(username='super_cooper',first_name='Jordan',last_name='Cooper',email='jc@stashit.com',password='password123',salt=random.randint(827,18273),profile_photo = 'default.png')
    db.session.add(user)
    user = User(username='becky',first_name='Alafia',last_name='Beckford',email='ab@stashit.com',password='password123',salt=random.randint(827,18273),profile_photo = 'default.png')
    db.session.add(user)
    user = User(username='nation',first_name='Shemara',last_name='Nation',email='sn@stashit.com',password='password123',salt=random.randint(827,18273),profile_photo = 'default.png')
    db.session.add(user)
    db.session.commit()
    return "users created"