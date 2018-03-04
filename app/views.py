"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, flash ,session ,abort
from .forms import reg_Form,login_Form,forgot_Form,upload_Form
from werkzeug.utils import secure_filename
from .controllers import get_uploaded_images,flash_errors,is_safe_url
from werkzeug.datastructures import CombinedMultiDict

"""
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
"""

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route("/")
def index():
    error = None
    return render_template('index.html',error=error)

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



@app.route("/login",methods=['POST', 'GET'])
def login():
    error = None
    login_form=login_Form()
    """ Handles application  login """  
    if request.method == 'POST':
        if login_form.validate_on_submit():
            # Login and validate the user.
            # user should be an instance of your `User` class
            
            #login_user(user)

            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))

    return render_template('login.html',error=error,login_form=login_form)

@app.route("/register",methods=['POST', 'GET'])
def register():
    error = None
    reg_form=reg_Form()
    if request.method == 'POST':

        """ Handles application registration """    
        if reg_form.validate_on_submit():    
            
            flash('You are registered', 'success')
            return redirect(url_for('dashboard'))
    return render_template('register.html',error=error,reg_form=reg_form)


@app.route("/forgot_pass",methods=['POST', 'GET'])
def forgot_pass():
    error = None
    forgot_form=forgot_Form()
    if request.method == 'POST':
        """ Handles application account recovery"""  
        if forgot_form.validate_on_submit():
            
            flash('You were logged in', 'success')
            return redirect(url_for('dashboard'))
    return render_template('forgot_pass.html',error=error,forgot_form=forgot_form)


@app.route("/busted")
def busted():
    return render_template('busted.html')


@app.route("/dashboard")
#@login_required
def dashboard():
    return render_template('feed.html')


@app.route('/logout', methods=['GET'])
#@login_required
def logout():
    logout_user()
    #session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('index'))

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