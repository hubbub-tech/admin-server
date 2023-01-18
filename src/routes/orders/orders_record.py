from datetime import datetime
from flask import Blueprint, g, request, make_response

from src.models import Orders
from src.models import Users
from src.models import Items

from src.utils.classes import Paginator

from src.utils.settings import (
    CODE_2_OK
)

from src.utils import login_required

bp = Blueprint('record', __name__)

@bp.get('/orders')
@login_required
def orders():

    try:
        page_number = int(request.args.get("page_number"))
        page_amount = int(request.args.get("page_amount"))
    except:
        page_number = 1
        page_amount = 25

    order_ids = Orders.get_ids(sort_by="id", descending=True)
    page_max = len(order_ids) / page_amount

    paginator = Paginator()
    chunk_order_ids = paginator.get_hits(order_ids, page_number, page_amount)

    orders_to_dict = []
    for order_id in chunk_order_ids:
        order = Orders.get({ "id": order_id })
        order_to_dict = order.to_dict()

        order_to_dict["ext_dt_start"] = datetime.timestamp(order.ext_dt_start)
        order_to_dict["ext_dt_end"] = datetime.timestamp(order.ext_dt_end)

        order_to_dict["total_charge"] = order.get_total_charge()
        order_to_dict["total_deposit"] = order.get_total_deposit()

        order_to_dict["dropoff_id"] = order.get_dropoff_id()
        order_to_dict["pickup_id"] = order.get_pickup_id()

        item = Items.get({ "id": order.item_id })
        renter = Users.get({ "id": order.renter_id })

        order_to_dict["item_name"] = item.name
        order_to_dict["renter_name"] = renter.name

        orders_to_dict.append(order_to_dict)

    orders_to_dict = sorted(orders_to_dict, key = lambda order: order["ext_dt_end"], reverse=True)

    data = { 
        "orders": orders_to_dict, 
        "page_max": page_max, 
        "page_number": page_number,
        "page_amount": page_amount
    }
    response = make_response(data, CODE_2_OK)
    return response


    
