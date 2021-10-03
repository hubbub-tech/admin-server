import os
from flask import Blueprint, g, request
from flask_cors import CORS
from blubber_orm import Users, Carts, Items
from blubber_orm import Orders, Reservations
from blubber_orm import Dropoffs, Pickups

from server.tools.settings import login_required
from server.tools.settings import Config, AWS
from server.tools.settings import json_sort

bp = Blueprint('manage_orders', __name__)
CORS(bp,
    origins=[Config.CORS_ALLOW_ORIGINS["admin"]],
    supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS
)

@bp.get('/orders')
@login_required
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
@login_required
def order_summary(order_id):
    photo_url = AWS.get_url("items")
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
    if dropoff:
        order_to_dict["dropoff"] = dropoff.to_dict()
        order_to_dict["dropoff"]["logistics"] = dropoff.logistics.to_dict()
    else:
        order_to_dict["dropoff"] = None

    if pickup:
        order_to_dict["pickup"] = pickup.to_dict()
        order_to_dict["pickup"]["logistics"] = pickup.logistics.to_dict()
    else:
        order_to_dict["pickup"] = None

    order_to_dict["ext_date_start"] = order.ext_date_start.strftime("%Y-%m-%d")
    order_to_dict["ext_date_end"] = order.ext_date_end.strftime("%Y-%m-%d")

    order_to_dict["renter"] = renter.to_dict()
    order_to_dict["renter"]["name"] = renter.name

    order_to_dict["lister"] = lister.to_dict()
    order_to_dict["lister"]["name"] = lister.name

    order_to_dict["item"] = item.to_dict()
    order_to_dict["item"]["details"] = item.details.to_dict()

    order_to_dict["extensions"] = extensions_to_dict
    order_to_dict["reservations"] = reservations_to_dict
    return {
        "order": order_to_dict,
        "photo_url": photo_url
    }

@bp.get('/commands/reminder/pickup')
@login_required
def pickup_reminder_command():
    orders = {}
    orders_not_picked = Orders.filter({"is_pickup_sched": False})
    for order in orders_not_picked:
        if date.today() < order.ext_date_end:
            if order.res_date_start <= date.today():
                if orders.get(order.renter_id):
                    orders[order.renter_id].append(order)
                else:
                    orders[order.renter_id] = [order]

    for renter_id in orders.keys():
        renter = Users.get(renter_id)
        rentals = orders[renter_id]
        print(rentals)
        print(renter.email)
        # email_data = get_pickup_schedule_reminder(renter, rentals)
        # send_async_email.apply_async(kwargs=email_data)
    return {"flashes": ["Emails bulk sent!"]}, 200

@bp.get('/commands/reminder/dropoff')
@login_required
def dropoff_reminder_command():
    return {"flashes": ["Emails bulk sent!"]}, 200

@bp.get('/commands/reminder/shopping')
@login_required
def shopping_reminder_command():
    shoppers = [] # Carts.get_shoppers()
    for shopper in shoppers:
        print(shopper.name)
        # email_data = get_shopping_cart_reminder(shopper)
        # send_async_email.apply_async(kwargs=email_data)
    return {"flashes": ["Emails bulk sent!"]}, 200
