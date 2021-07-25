import os
from flask import Blueprint, g, request
from flask_cors import CORS
from blubber_orm import Orders, Users, Reservations, Items
from blubber_orm import Dropoffs, Pickups

from server.tools.settings import Config
from server.tools.settings import json_sort

bp = Blueprint('admin', __name__)
CORS(bp, origins=[Config.CORS_ALLOW_ORIGINS["admin"]])

@bp.get('/orders')
def orders():
    orders = []
    db_orders = Orders.get_all()
    for order in db_orders:
        item = Items.get(order.item_id)
        renter = Users.get(order.renter_id)
        order_to_dict = order.to_dict()
        order_to_dict["item"] = item.to_dict()
        order_to_dict["renter"] = renter.to_dict()
        order_to_dict["renter"]["name"] = renter.name
        order_to_dict["reservation"] = order.reservation.to_dict()
        order_to_dict["ext_date_end"] = order.ext_date_end.strftime("%Y-%m-%d")
        orders.append(order_to_dict)
    json_sort(orders, "date_placed", reverse=True)
    return {"orders": orders}

@bp.get('/order/summary/id=<int:order_id>')
def order_summary(order_id):
    order = Orders.get(order_id)
    renter = Users.get(order.renter_id)
    lister = Users.get(order.lister_id)
    item = Items.get(order.item_id)
    dropoff = Dropoffs.by_order(order)
    pickup = Pickups.by_order(order)
    reservations_to_dict = [order.reservation.to_dict()]
    extensions = order.extensions
    extensions_to_dict = []
    for extension in extensions:
        extensions_to_dict.append(extension.to_dict())
        reservations_to_dict.append(extension.reservation.to_dict())

    order_to_dict = order.to_dict()
    order_to_dict["ext_date_start"] = order.ext_date_start.strftime("%Y-%m-%d")
    order_to_dict["ext_date_end"] = order.ext_date_end.strftime("%Y-%m-%d")

    order_to_dict["renter"] = renter.to_dict()
    order_to_dict["renter"]["name"] = renter.name

    order_to_dict["lister"] = lister.to_dict()
    order_to_dict["lister"]["name"] = lister.name

    order_to_dict["item"] = item.to_dict()

    order_to_dict["dropoff"] = dropoff.to_dict()
    order_to_dict["dropoff"]["logistics"] = dropoff.logistics.to_dict()

    order_to_dict["pickup"] = pickup.to_dict()
    order_to_dict["pickup"]["logistics"] = pickup.logistics.to_dict()

    order_to_dict["extensions"] = extensions_to_dict
    order_to_dict["reservations"] = reservations_to_dict
    return {"order": order_to_dict}
