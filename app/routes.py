from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime
from app import app, db
import os, string, random


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('login.html',  title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    return render_template('user.html', user=user, posts=posts, mode='user', title='Profile')

def randomString(number):
    hunk = string.ascii_letters
    res = ''
    for i in range(number):
        res += random.choice(hunk)
    return res
@app.route('/addpost', methods=['POST', 'GET'])
@login_required
def addpost():
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
        post = Post(title = form.title.data, filename = filename, description = form.description.data, user_id = user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addpost.html', title='Add an Image', form=form)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<post_id>')
def delete(post_id):
    if post_id:
        post = Post.query.get(post_id)
        if current_user.id == post.user_id:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.filename))
            db.session.delete(post)
            db.session.commit()
    return redirect(url_for('index'))
