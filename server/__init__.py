import os
from flask import Flask

from .tools.settings.config import Config

def create_app():
    config_object = Config()
    app = Flask(__name__)

    # Flask Config
    app.config.from_object(config_object)

    from .routes import admin
    app.register_blueprint(admin)

    return app
