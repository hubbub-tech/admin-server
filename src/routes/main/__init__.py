from flask import Blueprint
from flask_cors import CORS

from src.utils.settings import FlaskConfig

from .main_index import bp as main_index

bp = Blueprint("main", __name__)

bp.register_blueprint(main_index)

CORS(
    bp,
    origins=[FlaskConfig.CORS_ALLOW_ORIGIN],
    supports_credentials=FlaskConfig.CORS_SUPPORTS_CREDENTIALS
)
