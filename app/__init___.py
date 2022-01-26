# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from .gift_list import gift_list as gift_list_blueprint
    app.register_blueprint(gift_list_blueprint, url_prefix='/gift_list')

    return app
