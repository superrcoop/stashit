import os
from time import time
from flask_mail import Message, Mail
from app import app, db, mail , login_manager
from random import randint
from flask import render_template, request, redirect, url_for, flash ,session ,abort
from .forms import reg_Form,login_Form,forgot_Form,upload_Form, recoverForm, passwordForm,authForm,feedbackForm,urlForm
from werkzeug.utils import secure_filename
from .controllers import get_uploaded_images, regexPassword, regexAlpha, regexEmail, regexUsername, allowed_file
from werkzeug.datastructures import CombinedMultiDict
from .models import User
from flask_login import login_user, logout_user, login_required, current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    error = None
    return render_template('index.html',error=error)

@app.route("/settings",methods=['POST', 'GET'])
@login_required
def settings():
    error ,message = None,None
    form = authForm()
    form2=feedbackForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            auth = form.auth.data
            user=current_user
            if user and user.checkCode(auth):
                db.session.commit()
                return render_template('settings.html',message="Your account has been Authenticated",form=form)
            else:
                if user.is_authenticated:
                    message="Account is already authenticated"
                else:
                    error="Invalid authentication code"
        if form2.validate_on_submit():
            msg = Message("You have received feedback from "+current_user.username,
                    sender="stashit.no.reply@gmail.com",
                    recipients=["stashit.no.reply@gmail.com"])
            msg.body=form2.feedback.data
            mail.send(msg)
            return render_template('settings.html',message="Feedback has been sent",form2=form2)
    return render_template('settings.html',error=error,form=form,message=message,form2=form2)


@app.route("/login",methods=['POST', 'GET'])
def login():
    error = None
    form = login_Form()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if regexEmail(email) and regexPassword(password):
            user = User.query.filter_by(email = email).first()
            if user and user.is_correct_password(password): 
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else: 
                error = "Invalid email and/or password"
        else:
            error = "Invalid email and/or password"
    return render_template('login.html',error=error,form=form)

@app.route("/register",methods=['POST', 'GET'])
def register(): 
    error = None
    form = reg_Form()
    if request.method == 'POST' and form.validate_on_submit():
        first_name, last_name, email, password, conf_password, username = form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.conf_password.data, form.username.data
        if regexEmail(email) and regexPassword(password) :
            if regexAlpha(first_name) and regexAlpha(last_name) and regexUsername(username):
                if not User.query.filter_by(email = email).first() and not User.query.filter_by(username = username).first():
                    user = User(username = username, first_name = first_name, last_name = last_name, email = email, plain_password = password)
                    db.session.add(user)
                    db.session.commit()
                    msg = Message("Hi "+user.first_name+", Thank you for registering at Stashit.website",
                    sender="stashit.no.reply@gmail.com",
                    recipients=[user.email])
                    msg.body="Your authentication code is: "+str(user.recoveryCode)
                    mail.send(msg)
                    return render_template('login.html', message="Success, You should receive an email with an authentication code", form = login_Form())
                else:
                    error = "Email and/or username already exists"
            else:
                error="Invalid Name and/or Username"
        else:
            error = "Invalid email and/or password. Password must be of length 8 contain at least 1 upper,lower alphanumeric character and character (a-z,A-Z,0-9,!@#\$%\^&\*)"
    return render_template('register.html', error=error, form=form)

@app.route("/recovery", methods=['POST', 'GET'])
def recovery():
    error, message = None, None
    form = recoverForm()
    if request.method == 'POST' and form.validate_on_submit():
        email, recovery = form.email.data, form.recover.data
        if regexEmail(email):
            user = User.query.filter_by(email = email).first()
            if user and user.checkCode(recovery):
                db.session.commit()
                login_user(user)
                form = passwordForm()
                return render_template('changepassword.html', email = user.email, form = passwordForm(),message="Password recovery,New password must be of length 8 contain at least 1 upper,lower alphanumeric character and character (a-z,A-Z,0-9,!@#\$%\^&\*)")
            else:
                error = "Invalid recovery code"
        else:
            error = "Invalid email and/or recovery code"
    return render_template('recover.html', error = error, form = form)

@app.route("/forgot_pass",methods=['POST', 'GET'])
def forgot_pass():
    error, message = None, None
    form = forgot_Form()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        if regexEmail(email):
            user = User.query.filter_by(email = email).first()
            if user:
                msg =  Message('Did you forget your account details?', sender = 'stashit.no.reply@gmail.com', recipients = [user.email])
                msg.body = "Hi " + user.username + ", your recovery code is: " + user.recoveryCode + ". Happy Stashing."
                try:
                    mail.send(msg)
                    db.session.commit()
                except SMTPAuthenticationError:
                    return render_template('forgot_pass.html',error = "Internal Server Error. Please Try again.", form = form)
                return render_template('recover.html', message = "Email Successfully Sent.", form = recoverForm(), email = user.email)
            else:
                error = "Email address not found. You may create a new acount. It's FREE!"
        else:
            error = "Invalid email address"
    return render_template('forgot_pass.html',error = error, form = form, message = message)

@app.route('/changepassword', methods = ['POST', 'GET'])
@login_required
def changePassword():
    form = passwordForm()
    if request.method == "POST" and form.validate_on_submit():
        password, conf_password = form.password.data, form.conf_password.data
        if regexPassword(password):
            user = current_user
            user.password(password)
            db.session.commit()
            #flask fresh login can be applied here
            return redirect(url_for('logout'))
        else:
            error = "Invalid password. Password must be of length 8 contain at least 1 upper,lower alphanumeric character and character (a-z,A-Z,0-9,!@#\$%\^&\*)"
    return render_template('changepassword.html', email = current_user.email, form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('feed.html')

@app.route("/important")
@login_required
def important():
    error = None
    return render_template('important.html',error=error)

@app.route("/gallery")
@login_required
def gallery():
    error = None
    return render_template('gallery.html',error=error)

@app.route("/passwords")
@login_required
def passwords():
    error = None
    return render_template('passwords.html',error=error)

@app.route("/blockchain")
@login_required
def blockchain():
    error = None
    return render_template('blockchain.html',error=error)

@app.route("/documents")
@login_required
def documents():
    error = None
    return render_template('documents.html',error=error)

@app.route("/url")
@login_required
def url():
    error = None
    return render_template('url.html',error=error)


@app.route("/alerts")
@login_required
def alerts():
    return render_template('alerts.html')

@app.route("/messages")
@login_required
def messages():
    return render_template('messages.html')

@app.route("/busted")
def busted():
    return render_template('busted.html')


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    error,message=None,None
    form = upload_Form(CombinedMultiDict((request.files, request.form)))
    form2=passwordForm()
    form3=urlForm()
    form4= upload_Form(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.upload.data
            if file.filename == '':
                error='No selected file'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_user.file_URI, filename))
            else:
                 error='File not allowed'
            flash('File Saved', 'success')
            return render_template('upload.html',form=form,form2=form2,form3=form3,form4=form4,error=error)
        if form2.validate_on_submit():
            title=request.form2['title']
            password, conf_password = form2.password.data, form2.conf_password.data
            if regexPassword(password) and regexAlpha(title):
                #save to text file or database?
                return render_template('upload.html',form=form,form2=form2,form3=form3,form4=form4,error=error)

        if form3.validate_on_submit():
            return render_template('upload.html',form=form,form2=form2,form3=form3,form4=form4,error=error)

        if form4.validate_on_submit():
            return render_template('upload.html',form=form,form2=form2,form3=form3,form4=form4,error=error)


    return render_template('upload.html',form=form,form2=form2,form3=form3,form4=form4,error=error)

@app.route('/recent')
@login_required
def view_files():
    if not session.get('logged_in'):
        abort(401)
    files = get_uploaded_images()
    return render_template('recents.html', files = files)


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")