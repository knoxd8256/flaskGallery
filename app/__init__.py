"""
flaskGallery __init__.py
This script defines the app and imports a number of packages and variables necessary for Flask to operate.
"""

# Imports

# Import data from conifguration file
from config import Config

# Import Flask modules from their respective packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Flask app creation and configuration
app = Flask(__name__)
app.config.from_object(Config)

# Database stuff
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login stuff
login = LoginManager(app)
login.login_view = 'login'

# Due to the fact that app and db must be defined in this script, these imports must be down here.
from app import models  # noqa E402
from app import routes  # noqa E402
