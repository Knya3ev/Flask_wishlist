from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# local imports
from config import app_config

# db variable initialization
from instance.config import UPLOAD_FOLDER


db = SQLAlchemy()
login_manager = LoginManager()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)

    from app import models
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .gift_list import gift_list as gift_list_blueprint
    app.register_blueprint(gift_list_blueprint)

    return app
