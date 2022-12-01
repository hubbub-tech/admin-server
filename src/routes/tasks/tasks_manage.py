from datetime import datetime, timedelta
from flask import Blueprint, make_response, request

from src.models import Timeslots
from src.models import Logistics

from src.utils.settings import (
    CODE_2_OK,
    CODE_4_BAD_REQUEST,
    CODE_4_NOT_FOUND
)

bp = Blueprint("manage", __name__)

@bp.post('/task/set-time')
@login_required
def set_task_time():

    try:
        logistics_id = request.json["taskId"]
        dt_sched_eta_json = request.json["dtSched"]

        dt_range_start_json = request.json["dtRangeStart"]
        dt_range_end_json = request.json["dtRangeEnd"]
    except KeyError:
        error = "Your input is incomplete."
        response = make_response({ "message": error }, CODE_4_BAD_REQUEST)
        return response
    except Exception as e:
        rror = "Something went wrong. Please, try again."
        # NOTE: Log error here.
        response = make_response({ "message": error }, CODE_5_SERVER_ERROR)
        return response

    dt_sched_eta = datetime.fromtimestamp(float(dt_sched_eta_json))

    dt_range_start = datetime.fromtimestamp(float(dt_range_start_json))
    dt_range_end = datetime.fromtimestamp(float(dt_range_end_json))

    logistics = Logistics.get({ "id": logistics_id })

    if logistics is None:
        error = "This task does not exist."
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    timeslot_pkeys = {
        "logistics_id": logistics_id,
        "dt_range_start": dt_range_start,
        "dt_range_end": dt_range_end
    }

    timeslot = Timeslots.get(timeslot_pkeys)

    if timeslot is None:

        if dt_range_start >= dt_range_end:
            timeslot_pkeys["dt_range_end"] = dt_range_start + timedelta(hours=1)

        timeslot_data = timeslot_pkeys
        timeslot_data["is_sched"] = True
        timeslot_data["dt_sched_eta"] = dt_sched_eta

        timeslot = Timeslots.insert(timeslot_data)
    else:
        Timeslots.set(timeslot_pkeys, { "is_sched": True, "dt_sched_eta": dt_sched_eta })

    email_data = set_task_time_email(task, chosen_time)
    send_async_email.apply_async(kwargs=email_data)

    time_sched_eta_str = dt_sched_eta.strftime("%H:%M")
    date_sched_eta_str = dt_sched_eta.strftime("%b %-d, %Y")
    message = f"You have scheduled a delivery event for {time_sched_eta_str} on {date_sched_eta_str}."
    response = make_response({ "message": message }, CODE_2_OK)
    return response
