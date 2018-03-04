from wtforms import StringField, PasswordField  , HiddenField,BooleanField
from wtforms.validators import Required,Length, Email,EqualTo ,DataRequired
from flask_wtf import FlaskForm , RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

class login_Form(FlaskForm):
    email = StringField('Email Address', validators=[Email(message='This is not a valid email'), Length(min=6, max=40,message=('Email does not satisfy condition ( 6 < email.length <= 40 )')),Required('Please provide an email address')])
    password = PasswordField('Enter Password',validators=[DataRequired()])
    #accept_tos = BooleanField('Remember Me')

class reg_Form(FlaskForm):
    name = StringField('Name', validators=[Length(min=4, max=25,message=('Name does not satisfy condition ( 4 < name.length <= 25 )')),Required('Please provide a name')])
    email = StringField('Email Address', validators=[Email(message='This is not a valid email'), Length(min=6, max=40,message=('Email does not satisfy condition ( 6 < email.length <= 40 )')),Required('Please provide an email address')])
    password = PasswordField('Enter Password',validators=[DataRequired()])
    conf_password=PasswordField('Repeat Password',validators=[Required('Re-enter password')])
    accept_tos = BooleanField('I accept the Terms&conditions', validators=[DataRequired()])
    recaptcha = RecaptchaField()

class upload_Form(FlaskForm):
    upload = FileField('Upload', validators=[
        FileRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')
    ])

class forgot_Form(FlaskForm):
    email = StringField('Email Address', validators=[Email(message='This is not a valid email'), Length(min=6, max=40,message=('Email does not satisfy condition ( 6 < email.length <= 40 )')),Required('Please provide an email address')])
