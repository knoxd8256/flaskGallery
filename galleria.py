"""Main app file
This script loads the application to be run by Flask, and defines the shell context for 'flask shell'
"""
# Imports

# Importing app and database objects
from app import app
from app import db

# Importing User and Post objects
from app.models import User
from app.models import Post


@app.shell_context_processor
def make_shell_context():
    """This function defines the context for the 'flask shell' command."""
    return {'db': db, 'User': User, 'Post': Post}
