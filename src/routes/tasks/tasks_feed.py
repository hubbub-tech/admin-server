from datetime import datetime
from flask import Blueprint, make_response, request

from src.models import Users
from src.models import Orders
from src.models import Items
from src.models import Calendars
from src.models import Addresses

from src.utils.settings import aws_config
from src.utils.settings import CODE_2_OK

bp = Blueprint("feed", __name__)


@bp.get("/tasks/feed")
def task_feed():

    tasks = Logistics.get_all()

    tasks_to_dict = []
    for task in tasks:
        sender = Users.get({ "id": task.sender_id })
        receiver = Users.get({ "id": task.receiver_id })

        order_ids = task.get_order_ids()
        courier_ids = task.get_courier_ids()

        for order_id in order_ids:
            order = Orders.get({ "id": order_id })
            item = Items.get({ "id": order.item_id })

            order_to_dict = order.to_dict()
            order_to_dict["item"] = item.to_dict()
            order_to_dict["ext_dt_end"] = datetime.timestamp(order.ext_dt_end)

            orders_to_dict.append(order_to_dict)

        couriers_to_dict = []
        for courier_id in courier_ids:
            user = Users.get({ "id": courier_id })
            user_to_dict = user.to_dict()

            couriers_to_dict.append(user_to_dict)

        to_query_address = task.to_query_address("to")
        from_query_address = task.to_query_address("from")

        to_address = Addresses.get(to_query_address)
        from_address = Addresses.get(from_query_address)

        task_to_dict["to_addr_formatted"] = to_address.formatted
        task_to_dict["from_addr_formatted"] = from_address.formatted

        task_to_dict = task.to_dict()
        task_to_dict["sender"] = sender.to_dict()
        task_to_dict["receiver"] = receiver.to_dict()
        task_to_dict["orders"] = orders_to_dict
        task_to_dict["couriers"] = couriers_to_dict

        tasks_to_dict.append(task_to_dict)

    data = { "tasks": tasks_to_dict }
    response = make_response(data, 200)
    return response
