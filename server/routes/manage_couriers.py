import os
from flask import Blueprint, g, request
from flask_cors import CORS
from blubber_orm import Orders, Users, Reservations
from blubber_orm import Items, Details, Calendars
from blubber_orm import Dropoffs, Pickups

from server.tools.settings import Config, AWS
from server.tools.settings import json_sort

bp = Blueprint('manage_couriers', __name__)
CORS(bp, origins=[Config.CORS_ALLOW_ORIGINS["admin"]])

@bp.get('/orders/tasks')
def tasks():
    #TODO: return some json object of dropoffs/pickups which need to be made
    return {"tasks": tasks}
