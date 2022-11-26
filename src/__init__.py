import os
from flask import Flask

from .utils.settings.config import FlaskConfig

def create_app(config_object=FlaskConfig()):
    app = Flask(__name__)

    # Flask Config
    app.config.from_object(config_object)

    # Celery Worker Config
    from .utils.settings import celery
    celery.conf.update(app.config)

    from .routes import auth
    app.register_blueprint(auth)

    return app
