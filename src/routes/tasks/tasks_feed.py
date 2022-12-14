from datetime import datetime
from flask import Blueprint, make_response, request

from src.models import Users
from src.models import Orders
from src.models import Items
from src.models import Calendars
from src.models import Addresses
from src.models import Logistics, Timeslots

from src.utils.settings import aws_config
from src.utils.settings import CODE_2_OK

bp = Blueprint("feed", __name__)


@bp.get("/tasks/feed")
def task_feed():

    tasks = Logistics.filter({ "is_canceled": False })

    tasks_to_dict = []
    for task in tasks:
        sender = Users.get({ "id": task.sender_id })
        receiver = Users.get({ "id": task.receiver_id })

        order_ids = task.get_order_ids()
        courier_ids = task.get_courier_ids()
        timeslots = task.get_timeslots()

        task_to_dict = task.to_dict()
        task_to_dict["dt_due"] = None

        orders_to_dict = []
        for order_id in order_ids:
            order = Orders.get({ "id": order_id })
            item = Items.get({ "id": order.item_id })

            order_to_dict = order.to_dict()
            order_to_dict["item"] = item.to_dict()
            order_to_dict["ext_dt_end"] = datetime.timestamp(order.ext_dt_end)

            orders_to_dict.append(order_to_dict)

            if task_to_dict["dt_due"] is None:
                if order.renter_id == task.receiver_id:
                    task_to_dict["dt_due"] = datetime.timestamp(order.res_dt_start)
                else:
                    task_to_dict["dt_due"] = datetime.timestamp(order.ext_dt_end)

        couriers_to_dict = []
        for courier_id in courier_ids:
            user = Users.get({ "id": courier_id })
            user_to_dict = user.to_dict()

            couriers_to_dict.append(user_to_dict)

        timeslots_to_dict = []
        for time_range in timeslots:
            dt_range_start_index = 0
            dt_range_end_index = 1

            timeslot = Timeslots.get({
                "logistics_id": task.id,
                "dt_range_start": time_range[dt_range_start_index],
                "dt_range_end": time_range[dt_range_end_index]
            })

            if timeslot.dt_range_start <= datetime.timestamp(0): continue
            if timeslot.dt_range_end <= datetime.timestamp(0): continue
            if timeslot.dt_sched_eta <= datetime.timestamp(0): continue

            timeslot_to_dict = timeslot.to_dict()
            timeslots_to_dict.append(timeslot_to_dict)

        to_query_address = task.to_query_address("to")
        from_query_address = task.to_query_address("from")

        to_address = Addresses.get(to_query_address)
        from_address = Addresses.get(from_query_address)

        task_to_dict["to_addr_formatted"] = to_address.formatted
        task_to_dict["from_addr_formatted"] = from_address.formatted

        task_to_dict["sender"] = sender.to_dict()
        task_to_dict["receiver"] = receiver.to_dict()
        task_to_dict["orders"] = orders_to_dict
        task_to_dict["couriers"] = couriers_to_dict
        task_to_dict["timeslots"] = timeslots_to_dict

        tasks_to_dict.append(task_to_dict)

    data = { "tasks": tasks_to_dict }
    response = make_response(data, 200)
    return response
