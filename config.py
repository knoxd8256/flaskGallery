# Import os and define the basedir variable as the root directory of the flaskGallery app
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ This class defines certain configurations for the flask app.
        Attributes:
            SECRET_KEY: Secret key to be used for certain authorizations.
            SQLALCHEMY_DATABASE_URI: Location of SQL database.
            SQLALCHEMY_TRACK_MODIFICATIONS: Enables or disables change tracking feature on database.
            UPLOAD_FOLDER: Upload folder location.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'picuploads')
