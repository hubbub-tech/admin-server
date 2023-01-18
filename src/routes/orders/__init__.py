
from flask import Blueprint
from flask_cors import CORS

from src.utils.settings import FlaskConfig

from .orders_record import bp as orders_record
from .orders_manage import bp as orders_manage
from .orders_view import bp as orders_view

bp = Blueprint('orders', __name__)

bp.register_blueprint(orders_record)
bp.register_blueprint(orders_manage)
bp.register_blueprint(orders_view)

CORS(
    bp,
    origins=[FlaskConfig.CORS_ALLOW_ORIGIN],
    supports_credentials=FlaskConfig.CORS_SUPPORTS_CREDENTIALS
)
