from flask import Blueprint
from flask_cors import CORS

from src.utils.settings import FlaskConfig

from .tasks_feed import bp as tasks_feed
from .tasks_view import bp as tasks_view

bp = Blueprint('tasks', __name__)

bp.register_blueprint(tasks_feed)
bp.register_blueprint(tasks_view)

CORS(
    bp,
    origins=[FlaskConfig.CORS_ALLOW_ORIGIN],
    supports_credentials=FlaskConfig.CORS_SUPPORTS_CREDENTIALS
)
