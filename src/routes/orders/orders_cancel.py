from flask import Blueprint, g, request, make_response

from datetime import datetime

from src.models import Reservations
from src.models import Logistics
from src.models import Extensions
from src.models import Orders
from src.models import Users
from src.models import Items

from src.utils.settings import (
    CODE_2_OK,
    CODE_4_NOT_FOUND
)

from src.utils import login_required
from src.utils import get_cancellation_email
from src.utils import upload_email_data

bp = Blueprint('cancel', __name__)


@bp.get("orders/cancel")
@login_required
def cancel_order(order_id):

    order_id = request.args.get("order_id")
    order = Orders.get({"id": order_id})

    if order is None:
        error = "Sorry, we could not find this order. Please, try again."
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    if order.is_canceled:
        error = "Your order has been cancelled!"
        response = make_response({ "message": error }, CODE_2_OK)
        return response

    dropoff_id = order.get_dropoff_id()
    pickup_id = order.get_pickup_id()

    # START ORDER CANCELLATION SEQUENCE
    if dropoff_id:
        dropoff = Logistics.get({"id": dropoff_id})
        if dropoff.dt_sent and dropoff.dt_received is None:
            message = "It seems like your order is being delivered already. If this sounds wrong please contact us."
            response = make_response({"message": message}, CODE_2_OK)
            return response
        else:
            dropoff.remove_order(order.id)
            if dropoff.get_order_ids() == []:
                Logistics.set({"id": dropoff.id}, {"is_canceled": True})
                # WARNING: what happens if only one order is on the delivery?

    if pickup_id:
        pickup = Logistics.get({"id": pickup_id})
        if pickup.dt_sent and pickup.dt_received is None:
            message = "It seems like your order has been delivered already. If this sounds wrong please contact us."
            response = make_response({"message": message}, CODE_2_OK)
            return response
        else:
            pickup.remove_order(order.id)
            if pickup.get_order_ids() == []:
                Logistics.set({"id": pickup.id}, {"is_canceled": True})
                # WARNING: what happens if only one order is on the delivery?

    res_pkeys = order.to_query_reservation()
    reservation = Reservations.get(res_pkeys)

    reservation.archive(notes="Order canceled.")
    Reservations.set(res_pkeys, {"is_calendared": False})
    Orders.set({"id": order.id}, {"is_canceled": True})
    # END ORDER CANCELLATION SEQUENCE

    email_data = get_cancellation_email(order)
    upload_email_data(email_data, email_type="order_cancel")

    message = "Your order was successfully canceled!"
    response = make_response({"message": message}, CODE_2_OK)
    return response


@bp.post("/extensions/cancel")
@login_required
def cancel_extension():

    order_id = request.args.get("order_id")
    res_dt_start = request.args.get("res_dt_start")

    extension = Extensions.get({"id": order_id, "res_dt_start": res_dt_start})

    if extension is None:
        error = "Sorry, we could not find this order. Please, try again."
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    res_pkeys = extension.to_query_reservation()

    reservation = Reservations.get(res_pkeys)
    if reservation.is_calendared == False:
        error = "Your order has been cancelled!"
        response = make_response({ "message": error }, CODE_2_OK)
        return response

    order = Orders.get({"id": extension.order_id})
    pickup_id = order.get_pickup_id()

    # START EXTENSION CANCELLATION SEQUENCE
    if pickup_id:
        pickup = Logistics.get({"id": pickup_id})
        if pickup.dt_sent and pickup.dt_received is None:
            message = "It seems like your order has been delivered already. If this sounds wrong please contact us."
            response = make_response({"message": message}, CODE_2_OK)
            return response
        else:
            pickup.remove_order(order.id)
            if pickup.get_order_ids() == []:
                Logistics.set({"id": pickup.id}, {"is_canceled": True})
                # WARNING: what happens if only one order is on the delivery?

    reservation.archive(notes="Extension Canceled.")
    Reservations.set(res_pkeys, {"is_calendared": False})
    # END ORDER CANCELLATION SEQUENCE

    email_data = get_cancellation_email(extension)
    upload_email_data(email_data, email_type="extension_cancel")

    message = "Your extension was successfully canceled!"
    response = make_response({"message": message}, CODE_2_OK)
    return response



