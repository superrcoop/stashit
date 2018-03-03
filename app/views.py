"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, flash ,session ,abort
from forms import reg_Form,loginForm
from werkzeug.utils import secure_filename
from controller import *
from werkzeug.datastructures import CombinedMultiDict

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route("/busted")
def busted():
    return render_template('busted.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/dashboard")
def dashboard():
    return render_template('feed.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    form=loginForm()
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('dashboard'))
    return render_template('index.html', error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    form=reg_Form()
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('dashboard'))
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST', 'GET'])
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
            return redirect(url_for('home'))
        else:
            print form.errors.items()

            flash('File NOT Saved', 'error')
    return render_template('upload.html',form=form)

@app.route('/files')
def files():
    if not session.get('logged_in'):
        abort(401)
    files = get_uploaded_images()
    return render_template('files.html', files = files)

    
@app.route("/")
def index():
    return render_template('index.html')

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