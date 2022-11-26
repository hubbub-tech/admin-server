from datetime import datetime, date, timedelta

from blubber_orm import Orders, Users, Reservations
from blubber_orm import Items, Details, Calendars
from blubber_orm import Dropoffs, Pickups, Logistics

def create_task(dropoff=None, pickup=None):
    """Returns a json called 'task' to be manipulated by client"""
    if isinstance(dropoff, Dropoffs):
        task = {}
        task["type"] = "dropoff"
        task["task_date"] = dropoff.dropoff_date.strftime("%Y-%m-%d")
        task["address"] = dropoff.logistics.address.to_dict()
        task["logistics"] = dropoff.logistics.to_dict()
        task["is_complete"] = True

        renter = Users.get(dropoff.renter_id)
        task["renter"] = renter.to_dict()
        task["renter"]["name"] = renter.name
        task["renter"]["profile"] = renter.profile.to_dict()
        task["orders"] = []
        orders = Orders.by_dropoff(dropoff)
        if orders:
            for order in orders:
                order_to_dict = order.to_dict()
                item = Items.get(order.item_id)
                order_to_dict["item"] = item.to_dict()
                order_to_dict["item"]["details"] = item.details.to_dict()
                order_to_dict["reservation"] = order.reservation.to_dict()
                task["orders"].append(order_to_dict)
                if order.dt_dropoff_completed is None:
                    task["is_complete"] = False
        else:
            raise Exception("ERROR: why is there a dropoff without an order?")
    elif isinstance(pickup, Pickups):
        task = {}
        task["type"] = "pickup"
        task["task_date"] = pickup.pickup_date.strftime("%Y-%m-%d")
        task["address"] = pickup.logistics.address.to_dict()
        task["logistics"] = pickup.logistics.to_dict()
        task["is_complete"] = True

        renter = Users.get(pickup.renter_id)
        task["renter"] = renter.to_dict()
        task["renter"]["name"] = renter.name
        task["renter"]["profile"] = renter.profile.to_dict()
        task["orders"] = []
        orders = Orders.by_pickup(pickup)
        if orders:
            for order in orders:
                order_to_dict = order.to_dict()
                item = Items.get(order.item_id)
                order_to_dict["item"] = item.to_dict()
                order_to_dict["item"]["details"] = item.details.to_dict()
                order_to_dict["reservation"] = order.reservation.to_dict()
                task["orders"].append(order_to_dict)
                if order.dt_pickup_completed is None:
                    task["is_complete"] = False
        else:
            raise Exception("ERROR: why is there a dropoff without an order?")
    else:
        raise Exception("ERROR: you need to set either a pickup or a dropoff as an input.")
    return task
