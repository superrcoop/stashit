import os
from time import time
from flask_mail import Message, Mail
from app import app, db, mail
from random import randint
from flask import render_template, request, redirect, url_for, flash ,session ,abort
from .forms import reg_Form,login_Form,forgot_Form,upload_Form, recoverForm, passwordForm
from werkzeug.utils import secure_filename
from .controllers import get_uploaded_images, flash_errors, is_safe_url, checkPassword, checkAlpha, checkEmail
from werkzeug.datastructures import CombinedMultiDict
from models import User
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    error = None
    return render_template('index.html',error=error)

@app.route("/login",methods=['POST', 'GET'])
def login():
    error = None
    form = login_Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            if(checkPassword(password) and checkEmail(email)):
                user = User.query.filter_by(email = email).first()
                if user:
                    if user.checkPassword(password): 
                        login_user(user)
                        return redirect(url_for('dashboard'))
                    else: 
                        error = 'Invalid password. Please try again.'
                else:
                    error = 'Email address not found'
            else:
                error = "Invalid email and/or password. Please try again"
        else:
            error = "Oops! Try that again."
    else:
        pass
    return render_template('login.html',error=error,form=form)

@app.route("/register",methods=['POST', 'GET'])
def register(): 
    error = None
    form = reg_Form()
    if request.method == 'POST':    
        if form.validate_on_submit():
            first_name, last_name, email, password, conf_password, username = [form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.conf_password.data, form.username.data]
            if(checkEmail(email) and checkPassword(password) and checkPassword(conf_password) and checkAlpha(first_name), checkAlpha(last_name), checkAlpha(username)):
                if(password == conf_password):
                    if not User.query.filter_by(email = email).first() and not User.query.filter_by(username = username).first():
                        user = User(username = username, first_name = first_name, last_name = last_name, email = email, password = password, salt = randint(827,18273))
                        db.session.add(user)
                        db.session.commit()
                        return render_template('login.html', message="Success", form = login_Form())
                    else:
                        error = ""
                        if User.query.filter_by(email = email).first():
                            error += "Email address already exists. "
                        if User.query.filter_by(username = username).first():
                            error += "Username already exists."
                else: 
                    error = "Passwords didn't match. Please try again."
            else:
                error = "Please check your inputs and try again"
        else:
            error = "Oops! Try that again."
    else:
        pass 
    return render_template('register.html', error=error, form=form)

@app.route("/recovery", methods=['POST', 'GET'])
def recovery():
    error, message = None, None
    form = recoverForm()
    if request.method == 'POST': 
        if form.validate_on_submit():
            try:
                email, recovery = form.email.data, int(form.recover.data)
                if checkEmail(email):
                    user = User.query.filter_by(email = email).first()
                    if user:
                        if int(user.recoveryCode) == recovery:
                            user.recoveryCode = None
                            db.session.commit()
                            login_user(user)
                            form = passwordForm()
                            return render_template('changepassword.html', email = user.email, form = form)
                        else:
                            error = "Invalid recovery code. Please try again."
                    else:
                        error = "Internal Server Error. Please try again."
                else:
                    form = forgot_Form()
                    return render_template('forgot_pass.html',error = "Invalid email provided. Please start over the process.", form = form, message = None)
            except ValueError:
                error = "Invalid recovery code. Please try again."
        else:
            error = error + " Invalid form data"
    else: 
        error = "Hello world"
    # return redirect(url_for('forgot_pass'))
    return render_template('recover.html', error = error, form = form, email = "jc@stashit.com")
    form = forgot_Form()
    return render_template('forgot_pass.html',error = error, form = form, message = message)

@app.route("/forgot_pass",methods=['POST', 'GET'])
def forgot_pass():
    error, message = None, None
    form = forgot_Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            if checkEmail(email):
                user = User.query.filter_by(email = email).first()
                if user:
                    l = long(time())
                    msg =  Message('Recover Account', sender = 'stashit.no.reply@gmail.com', recipients = [email])
                    msg.body = "Hello " + user.first_name + ", your recovery code is " + str(l) + ". Happy Stashing."
                    try:
                        mail.send(msg)
                        user.recoveryCode = l
                        db.session.commit()
                    except SMTPAuthenticationError:
                        return render_template('forgot_pass.html',error = "Internal Server Error. Please Try again.", form = form, message = message)
                    form = recoverForm()
                    return render_template('recover.html', message = "Email Successfully Sent.", form = form, email = user.email)
                else:
                    error = "No account is tied to that account. You may create a new acount. It's FREE!"
            else:
                error = "Invalid email address. Please try again."
        else: 
            error = "Oops. Try that again"
    return render_template('forgot_pass.html',error = error, form = form, message = message)

@app.route('/changepassword', methods = ['POST', 'GET'])
@login_required
def changePassword():
    form = passwordForm()
    if request.method == "POST" and current_user :
        if form.validate_on_submit():
            password, conf_password = form.password.data, form.conf_password.data
            if checkPassword(password) and checkPassword(conf_password):
                if(password == conf_password):
                    user = current_user
                    user.changePassword(password)
                    db.session.commit()
                    return redirect(url_for('logout'))

                else:
                    error = "Passwords did not match, Please try again"
            else:
                error = "Invalid data. Please try again"
        else:
            pass
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
def important():
    error = None
    return render_template('important.html',error=error)

@app.route("/gallery")
def gallery():
    error = None
    return render_template('gallery.html',error=error)

@app.route("/passwords")
def passwords():
    error = None
    return render_template('passwords.html',error=error)

@app.route("/settings")
def settings():
    error = None
    return render_template('settings.html',error=error)

@app.route("/trash")
def trash():
    error = None
    return render_template('trash.html',error=error)

@app.route("/wallet_keys")
def wallet_keys():
    error = None
    return render_template('wallet_keys.html',error=error)

@app.route("/documents")
def documents():
    error = None
    return render_template('documents.html',error=error)

@app.route("/articles")
def articles():
    error = None
    return render_template('articles.html',error=error)

@app.route("/busted")
def busted():
    return render_template('busted.html')


@app.route('/upload', methods=['POST', 'GET'])
#@login_required
def upload():
    if not session.get('logged_in'):
        abort(401)

    form = UploadForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST':
        if form.validate_on_submit():
            f = form.upload.data
            filename = secure_filename(f.filename)
                # Get file data and save to your uploads folder
            f.save(os.path.join(
                            app.config['UPLOAD_FOLDER'], filename
                        ))
            flash('File Saved', 'success')
            return redirect(url_for('dashboard'))
        flash('File NOT Saved', 'error')
        return redirect(url_for('dashboard'))
    return render_template('upload.html',form=form)

@app.route('/recent')
#@login_required
def view_files():
    if not session.get('logged_in'):
        abort(401)
    files = get_uploaded_images()
    return render_template('recents.html', files = files)

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