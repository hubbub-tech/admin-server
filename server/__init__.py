import os
from flask import Flask

from .tools.settings.config import Config

def create_app():
    config_object = Config()
    app = Flask(__name__)

    # Flask Config
    app.config.from_object(config_object)

    from .routes import manage_couriers, manage_items, manage_orders
    app.register_blueprint(manage_couriers)
    app.register_blueprint(manage_items)
    app.register_blueprint(manage_orders)

    return app
