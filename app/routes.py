"""Routing file

This script routes requests for specific URLs through Flask's rendering engine and returns the requested content.
This file should ONLY be used with the full flaskGallery package, or most of the routes will return errors or nothing.

This file contains routes decorated with the app.route decorator, as well as a short random string generator function.
These routes and functions are as listed below:
    * index() - Homepage route
    * login() - Login form and handler route
    * register() - Register form and handler route
    * logout() - Logout handler route
    * user() - Profile page route
    * addpost() - Post submission form and handler route
    * uploaded_file() - Uploaded file retrieval route
    * delete() - File deletion handler route
    * randomString() - Random string generator
"""

# Imports

# Import generic python modules to interact with the system and manipulate variables
import os
import random
import string

# Import application and database data
from app import app
from app import db

# Import forms defined in forms.py
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import PostForm

# Import database table models
from app.models import User
from app.models import Post

# Import date and time objects
from datetime import datetime

# Import flask methods and decorators for route definition and resolution
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import send_from_directory

# Import login handling functions
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

# Import url parser
from werkzeug.urls import url_parse

# Routes


# Homepage Route
@app.route('/')
@app.route('/index')
def index():
    """Homepage route to display all posted images.

    Returns:
        .html file: Rendered gallery with all posted images by all users.
    """
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route to display and handle login form.

    Returns:
        .html file: Rendered page to login a user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route to display and handle registration form.

    Returns:
        .html file: Rendered page to register a user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Logout Route
@app.route('/logout')
@login_required
def logout():
    """Logs out the current user and returns to the Homepage.

    Returns:
        redirect: A redirection to the /index route.
    """
    logout_user()
    return redirect(url_for('index'))

# User Profile Route
@app.route('/user/<username>')
@login_required
def user(username):
    """User Profile page to display posts by a given user.

    Args:
        username (str): The user to be displayed. Specified at '/user/<username>'.

    Returns:
        .html file: Rendered profile page with all posted images displayed.
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    return render_template('user.html', user=user, posts=posts, mode='user', title='Profile')

# Post Submission Route
@app.route('/addpost', methods=['POST', 'GET'])
@login_required
def addpost():
    """Post submission route to return the post submission form and handle data once submitted.

    Returns:
        .html file: Rendered post submission form.
    """
    user = current_user
    form = PostForm()
    if form.validate_on_submit():
        if request.files['image']:
            image = request.files['image']
        else:
            image = 'Not Found'
        filename = randomString(15)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(path):
            filename += randomString(2)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)
        post = Post(title=form.title.data, filename=filename, description=form.description.data, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addpost.html', title='Add an Image', form=form)

# Uploaded File Route
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Upload Fetcher - returns a requested file from the uploads folder.

    Args:
        filename (str): Filename associated with the desired file.

    Returns:
        file: File requested from the uploads folder.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Post Deletion Route
@app.route('/delete/<post_id>')
def delete(post_id):
    """Post Deletion Function

    Args:
        post_id (int): Post ID as defined in the Post table of the database.

    Returns:
        redirect: Redirection to the homepage.
    """
    if post_id:
        post = Post.query.get(post_id)
        if current_user.id == post.user_id:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.filename))
            db.session.delete(post)
            db.session.commit()
    return redirect(url_for('index'))


# Random String Generator
def randomString(number):
    """Random String Generator.

    Args:
        number (int): Number of characters to be generated.

    Returns:
        str: Randomly generated string of upper- and lower-case ASCII letters.
    """

    hunk = string.ascii_letters
    res = ''
    for i in range(number):
        res += random.choice(hunk)
    return res
