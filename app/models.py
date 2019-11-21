"""Models File

This script defines classes for User() and Post() objects, and defines the load_user() function.
These classes and functions are as listed below:
    * load_user() - Loads a user by id number.
    * User() - Definition of a User() class which is able to be directly inserted into a User table, which can be generated from said class.
    * Post() - Definition of a Post() class which is able to be directly inserted into a Post table, which can be generated from said class.
"""
# Imports

# Import database and login objects
from app import db
from app import login

# Import user mixin class
from flask_login import UserMixin

# Import password methods from werkzeug
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# User retrieval function
@login.user_loader
def load_user(id):
    """User loader.

    Args:
        id (int): User ID as specified in the database entry.

    Returns:
        user (object): User data retrieved from User table.
    """
    return User.query.get(int(id))


# User Class
class User(UserMixin, db.Model):
    """User Table entry model.

    Args:
        UserMixin (class): UserMixin Class to inherit from. (Flask-Login)
        db.Model (object): Database table model to inherit from. (SQLAlchemy)

    Attributes:
        id (int): User ID.
        username (str): Username.
        password_hash (str): Hashed password.
        posts (relationship): All posts which were made by this user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Password setter method."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Password checker method."""
        return check_password_hash(self.password_hash, password)


# Post Class
class Post(db.Model):
    """Post Table entry model.

    Args:
        db.Model (object): Database table model to inherit from. (SQLAlchemy)

    Attributes:
        id (int): Post ID.
        title (str): Post title.
        filename (str): Filename of image attached to post.
        description (str): Description / Body of post.
        user_id (int): ID of user who created this post.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    filename = db.Column(db.String(128))
    description = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
