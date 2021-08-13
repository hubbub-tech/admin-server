import os
from flask import Blueprint, g, request
from flask_cors import CORS

from datetime import datetime, date, timedelta
from blubber_orm import Orders, Users, Reservations
from blubber_orm import Items, Details, Calendars
from blubber_orm import Dropoffs, Pickups, Logistics

from server.tools.build import create_task, complete_task
from server.tools.settings import Config, AWS
from server.tools.settings import json_sort

bp = Blueprint('manage_tasks', __name__)
CORS(bp, origins=[Config.CORS_ALLOW_ORIGINS["admin"]])

@bp.get('/tasks')
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
        update_time = {"chosen_time": chosen_time}
        Logistics.set(logistics_keys, update_time)
        #TODO: send an email with the chosen time to parties involved
        return {"flashes": [f"The time you chose, {chosen_time_json} for {task['type']} on {task['task_date']} has been set successfully."]}, 200
    return {"flashes": ["This task cannot be completed."]}, 406

@bp.get('/task/dropoff/id=<int:order_id>')
def task_dropoff(order_id):
    order = Orders.get(order_id)
    dropoff = Dropoffs.by_order(order)
    if dropoff:
        if dropoff.dropoff_date > date.today():
            task = create_task(dropoff=dropoff)
            return {"task": task}
    return {"flashes": ["This task is not ready to complete."]}, 406

@bp.get('/task/pickup/id=<int:order_id>')
def task_pickup(order_id):
    order = Orders.get(order_id)
    pickup = Pickups.by_order(order)
    if pickup:
        if pickup.pickup_date > date.today():
            task = create_task(pickup=pickup)
            return {"task": task}
    return {"flashes": ["This task is not ready to complete."]}, 406

@bp.post('/task/dropoff/complete')
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
            if response["is_valid"] == False:
                return {"flashes": [response["message"]]}, 406
        return {"flashes": [f"All the orders for {task['type']} on {task['task_date']} have been completed."]}, 200
    return {"flashes": ["This task cannot be completed."]}, 406

@bp.post('/task/pickup/complete')
def complete_task_pickup():
    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    data = request.json
    if data:
        task = data["task"]
        pickup_date = datetime.strptime(task["task_date"], date_format).date()
        dt_sched = datetime.strptime(task["logistics"]["dt_scheduled"], datetime_format)
        pickup = Pickups.get({
            "dt_sched": dt_sched,
            "pickup_date": pickup_date,
            "renter_id": task["logistics"]["renter_id"]
        })
        for order_dict in task["orders"]:
            order = Orders.get(order_dict["id"])
            response = complete_task(order, pickup)
            if response["is_valid"] == False:
                return {"flashes": [response["message"]]}, 406
        return {"flashes": [f"All the orders for {task['type']} on {task['task_date']} have been completed."]}, 200
    return {"flashes": ["This task cannot be completed."]}, 406
