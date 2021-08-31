import os
from flask import Blueprint, g, request
from flask_cors import CORS

from datetime import datetime, date, timedelta
from blubber_orm import Orders, Users, Reservations
from blubber_orm import Items, Details, Calendars
from blubber_orm import Dropoffs, Pickups, Logistics
from blubber_orm import Addresses

from server.tools.build import get_task_time_email, update_task_time_email
from server.tools.build import get_task_confirmation_email, send_async_email
from server.tools.build import create_task, complete_task

from server.tools.settings import login_required
from server.tools.settings import Config, AWS
from server.tools.settings import json_sort

bp = Blueprint('manage_tasks', __name__)
CORS(bp,
    origins=[Config.CORS_ALLOW_ORIGINS["admin"]],
    supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS
)

@bp.get('/tasks')
@login_required
def tasks():
    #TODO: return some json object of dropoffs/pickups which need to be made
    all_dropoffs = Dropoffs.get_all()
    all_pickups = Pickups.get_all()
    tasks = []
    for dropoff in all_dropoffs:
        if dropoff.dropoff_date > date.today():
            task = create_task(dropoff=dropoff)
            if task["is_complete"] == False:
                tasks.append(task)

    for pickup in all_pickups:
        if pickup.pickup_date > date.today():
            task = create_task(pickup=pickup)
            if task["is_complete"] == False:
                tasks.append(task)
    json_sort(tasks, "task_date")
    return {"tasks": tasks}

@bp.post('/task/chosen-time')
@login_required
def set_task_time():
    date_format = "%Y-%m-%d"
    time_format = "%I:%M:00 %p"
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    data = request.json
    if data:
        task = data['task']
        chosen_time_json = data['chosenTime']
        chosen_time = datetime.strptime(chosen_time_json, time_format).time()
        dt_sched = datetime.strptime(task["logistics"]["dt_scheduled"], datetime_format)
        logistics_keys = {
            "dt_sched": dt_sched,
            "renter_id": task["logistics"]["renter_id"]
        }
        update_time = { "chosen_time": chosen_time }
        logistics = Logistics.get(logistics_keys)
        if logistics.chosen_time: is_chosen_time = True
        else: is_chosen_time = False

        Logistics.set(logistics_keys, update_time)
        if is_chosen_time:
            email_data = update_task_time_email(task, chosen_time)
        else:
            email_data = get_task_time_email(task, chosen_time)
        send_async_email.apply_async(kwargs=email_data)
        #TODO: send an email with the chosen time to parties involved
        return {"flashes": [f"The time you chose, {chosen_time_json} for {task['type']} on {task['task_date']} has been set successfully."]}, 200
    return {"flashes": ["This task cannot be completed."]}, 406

@bp.get('/task/dropoff/id=<int:order_id>')
@login_required
def task_dropoff(order_id):
    order = Orders.get(order_id)
    dropoff = Dropoffs.by_order(order)
    if dropoff:
        if dropoff.dropoff_date > date.today():
            task = create_task(dropoff=dropoff)
            return {"task": task}
    return {"flashes": ["This task is not ready to complete."]}, 406

@bp.get('/task/pickup/id=<int:order_id>')
@login_required
def task_pickup(order_id):
    order = Orders.get(order_id)
    pickup = Pickups.by_order(order)
    if pickup:
        if pickup.pickup_date > date.today():
            task = create_task(pickup=pickup)
            return {"task": task}
    return {"flashes": ["This task is not ready to complete."]}, 406

@bp.post('/task/dropoff/complete')
@login_required
def complete_task_dropoff():
    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    data = request.json
    if data:
        task = data["task"]
        dropoff_date = datetime.strptime(task["task_date"], date_format).date()
        dt_sched = datetime.strptime(task["logistics"]["dt_scheduled"], datetime_format)
        dropoff = Dropoffs.get({
            "dt_sched": dt_sched,
            "dropoff_date": dropoff_date,
            "renter_id": task["logistics"]["renter_id"]
        })
        for order_dict in task["orders"]:
            order = Orders.get(order_dict["id"])
            response = complete_task(order, dropoff)
            #TODO: youre thing was dropped off
            if response["is_valid"] == False:
                return {"flashes": [response["message"]]}, 406

            address_to_dict = task["address"]
            email_data = get_task_confirmation_email(task, address_to_dict)
            send_async_email.apply_async(kwargs=email_data)
        return {"flashes": [f"All the orders for {task['type']} on {task['task_date']} have been completed."]}, 200
    return {"flashes": ["This task cannot be completed."]}, 406

@bp.post('/task/pickup/complete')
@login_required
def complete_task_pickup():
    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    data = request.json
    if data:
        task = data["task"]
        address_keys = {
            "num": data["address"]["num"],
            "street": data["address"]["street"],
            "city": data["address"]["city"],
            "zip": data["address"]["zip_code"],
            "state": data["address"]["state"],
            "apt": data["address"]["apt"],
        }
        address = Addresses.filter(address_keys)
        if address:
            address, = address
        else:
            address = Addresses.insert(address_keys)

        pickup_date = datetime.strptime(task["task_date"], date_format).date()
        dt_sched = datetime.strptime(task["logistics"]["dt_scheduled"], datetime_format)
        pickup = Pickups.get({
            "dt_sched": dt_sched,
            "pickup_date": pickup_date,
            "renter_id": task["logistics"]["renter_id"]
        })
        for order_dict in task["orders"]:
            order = Orders.get(order_dict["id"])
            response = complete_task(order, pickup, address)
            #TODO: youre thing was picked up
            if response["is_valid"] == False:
                return {"flashes": [response["message"]]}, 406

            address_to_dict = address.to_dict()
            email_data = get_task_confirmation_email(task, address_to_dict)
            send_async_email.apply_async(kwargs=email_data)
        return {"flashes": [f"All the orders for {task['type']} on {task['task_date']} have been completed."]}, 200
    return {"flashes": ["This task cannot be completed."]}, 406
