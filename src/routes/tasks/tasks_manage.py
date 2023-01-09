from datetime import datetime, timedelta
from flask import Blueprint, make_response, request

from src.models import Timeslots
from src.models import Logistics

from src.utils import login_required
# from src.utils import send_async_email
# from src.utils import set_task_time_email


from src.utils.settings import (
    CODE_2_OK,
    CODE_4_BAD_REQUEST,
    CODE_4_NOT_FOUND,
    CODE_5_SERVER_ERROR
)

bp = Blueprint("manage", __name__)

@bp.post('/task/set-time')
@login_required
def set_task_time():

    try:
        dt_due_json = request.json["dtDue"]
        logistics_id = request.json["taskId"]
        time_sched_eta_str = request.json["timeSched"]

    except KeyError:
        error = "Your input is incomplete."
        response = make_response({ "message": error }, CODE_4_BAD_REQUEST)
        return response
    except Exception as e:
        error = "Something went wrong. Please, try again."
        # NOTE: Log error here.
        response = make_response({ "message": error }, CODE_5_SERVER_ERROR)
        return response

    date_due = datetime.fromtimestamp(float(dt_due_json)).date()
    time_sched_eta = datetime.strptime(time_sched_eta_str, "%H:%M").time()

    dt_sched_eta = datetime.combine(date_due, time_sched_eta)

    logistics = Logistics.get({ "id": logistics_id })

    if logistics is None:
        error = "This task does not exist."
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    ts_log_id, ts_dt_range_start, ts_dt_range_end = logistics.get_sched_timeslot()
    if ts_log_id:
        Timeslots.set({
            "logistics_id": ts_log_id,
            "dt_range_start": ts_dt_range_start,
            "dt_range_end": ts_dt_range_end
        }, { "is_sched": False, "dt_sched_eta": None })

    timeslots = Timeslots.filter({ "logistics_id": logistics_id })

    is_sched = False
    for timeslot in timeslots:
        if timeslot.dt_range_start < dt_sched_eta and \
            dt_sched_eta < timeslot.dt_range_end:

            is_sched = True
            Timeslots.set({
                "logistics_id": timeslot.logistics_id,
                "dt_range_start": timeslot.dt_range_start,
                "dt_range_end": timeslot.dt_range_end
            }, { "is_sched": is_sched, "dt_sched_eta": dt_sched_eta })
            break

    if is_sched == False:
        timeslot_data = {}
        timeslot_data["logistics_id"] = logistics.id
        timeslot_data["dt_range_start"] = dt_sched_eta - timedelta(hours=1)
        timeslot_data["dt_range_end"] = dt_sched_eta + timedelta(hours=1)
        timeslot_data["dt_sched_eta"] = dt_sched_eta
        timeslot_data["is_sched"] = True

        timeslot = Timeslots.insert(timeslot_data)

    # email_data = set_task_time_email(task, chosen_time)
    # send_async_email.apply_async(kwargs=email_data)

    time_sched_eta_str = dt_sched_eta.strftime("%H:%M")
    date_sched_eta_str = dt_sched_eta.strftime("%b %-d, %Y")
    message = f"You have scheduled a delivery event for {time_sched_eta_str} on {date_sched_eta_str}."
    response = make_response({ "message": message }, CODE_2_OK)
    return response
