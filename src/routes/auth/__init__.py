from flask import Blueprint
from flask_cors import CORS

from src.utils.settings import FlaskConfig

from .auth_login import bp as auth_login

bp = Blueprint('auth', __name__)

bp.register_blueprint(auth_login)

CORS(
    bp,
    origins=[FlaskConfig.CORS_ALLOW_ORIGIN],
    supports_credentials=FlaskConfig.CORS_SUPPORTS_CREDENTIALS
)
