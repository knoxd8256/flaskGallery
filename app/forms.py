"""Forms File

This script defines classes for all forms contained within the galleria app.
These classes are as listed below:
    * LoginForm()
    * RegistrationForm()
    * PostForm()
"""
# Imports

# Importing User model
from app.models import User

# Importing form fields and models from Flask WTF
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired

# Importing form fields and validators from WTForms
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import TextAreaField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from wtforms.validators import EqualTo
from wtforms.validators import Length


class LoginForm(FlaskForm):
    """A simple login form.

    Attributes:
        username (StringField): Username to log in as.
        password (PasswordField): Password for username.
        submit (SubmitField): Submit button.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """A user registration form.

    Attributes:
        username (StringField): Username to register user as.
        password (PasswordField): Password to set to username.
        password2 (PasswordField): Password verification, checks against password.
        submit (SubmitField): Submit button.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Validates whether a username is registered already or not.

        Args:
            username (str): Username to be tested.

        Raises:
            ValidationError: This error is raised if the username is in use.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    """A simple post submission form.

    Attributes:
        title (StringField): Title of post.
        description (TextAreaField): Description/body of post.
        image (FileField): Image to upload.
        submit (SubmitField): Submit button.
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=140)], render_kw={"rows": '5', "cols": '30'})
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField('Submit')
