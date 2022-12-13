from datetime import datetime
from flask import Blueprint, make_response, request

from src.models import Users
from src.models import Orders
from src.models import Items
from src.models import Calendars
from src.models import Addresses
from src.models import Logistics
from src.models import Timeslots

from src.utils.settings import aws_config
from src.utils.settings import CODE_2_OK, CODE_4_NOT_FOUND


bp = Blueprint("view", __name__)


@bp.get("/task/<int:logistics_id>")
def view_task(logistics_id):
    task = Logistics.get({ "id": logistics_id })

    if task.is_canceled:
        error = "Looks like this order has been canceled."
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    order_ids = task.get_order_ids()
    courier_ids = task.get_courier_ids()
    timeslots = task.get_timeslots()

    task_to_dict = task.to_dict()
    task_to_dict["dt_due"] = None

    orders_to_dict = []
    for order_id in order_ids:
        order = Orders.get({ "id": order_id })

        item = Items.get({ "id": order.item_id })
        item_calendar = Calendars.get({ "id": item.id })

        order_to_dict = order.to_dict()
        order_to_dict["item"] = item.to_dict()
        order_to_dict["item"]["image_url"] = aws_config.get_base_url() + f"/items/{item.id}.jpg"
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

        if timeslot.dt_range_start == datetime.min: continue
        if timeslot.dt_range_end == datetime.min: continue

        timeslot_to_dict = timeslot.to_dict()
        timeslots_to_dict.append(timeslot_to_dict)

    sender = Users.get({ "id": task.sender_id })
    receiver = Users.get({ "id": task.receiver_id })

    task_to_dict["sender"] = sender.to_dict()
    task_to_dict["receiver"] = receiver.to_dict()

    to_query_address = task.to_query_address("to")
    from_query_address = task.to_query_address("from")

    to_address = Addresses.get(to_query_address)
    from_address = Addresses.get(from_query_address)

    task_to_dict["to_addr_formatted"] = to_address.formatted
    task_to_dict["from_addr_formatted"] = from_address.formatted

    dt_sched_eta = task.get_dt_sched_eta()
    if isinstance(dt_sched_eta, datetime):
        task_to_dict["dt_sched_eta"] = datetime.timestamp(dt_sched_eta)
    else:
        task_to_dict["dt_sched_eta"] = None

    data = {
        "task": task_to_dict,
        "couriers": couriers_to_dict,
        "orders": orders_to_dict,
        "timeslots": timeslots_to_dict
    }
    response = make_response(data, CODE_2_OK)
    return response
