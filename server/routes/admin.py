import os
from flask import Blueprint, g, request
from flask_cors import CORS
from blubber_orm import Orders

from server.tools.settings import Config

bp = Blueprint('main', __name__)
CORS(bp, origins=[Config.CORS_ALLOW_ORIGINS["admin"]])

@bp.get('/orders')
def orders():
    orders = Orders.get_all()
    return {"orders": orders}
