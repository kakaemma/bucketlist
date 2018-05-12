from flask_api import FlaskAPI
from instance.config import application_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(application_config[config_name])
    app.config.from_pyfile('config.py')

    return app