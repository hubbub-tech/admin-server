from datetime import datetime
from flask import Blueprint, g, request, make_response

from src.models import Extensions
from src.models import Orders
from src.models import Items

from src.utils import safe_swap_items

from src.utils.settings import (
    CODE_2_OK,
    CODE_4_NOT_FOUND
)

from src.utils import login_required

bp = Blueprint('manage', __name__)

@bp.post('/orders/swap/<int:order_id>')
@login_required
def swap_on_order(order_id):
    order = Orders.get({ "id": order_id })

    if order is None:
        error = "This order does not exist." 
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    try:
        swap_item_id = request.json.get("swapItemId")
        swap_item = Items.get({ "id": swap_item_id })
    except:
        error = "Sorry, the item or renter you want to swap with does not exist."
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    status = safe_swap_items(order, swap_item)
    response = make_response({ "message": status.message }, CODE_2_OK)
    return  response


@bp.post('/extensions/swap/<int:order_id>')
@login_required
def swap_on_extension(order_id):

    try:
        swap_item_id = request.json.get("swapItemId")
        swap_item = Items.get({ "id": swap_item_id })

        ext_dt_start_json = request.json.get("extDtStart")
        ext_dt_start = datetime.fromtimestamp(float(ext_dt_start_json))
    except:
        error = "Sorry, the item or renter you want to swap with does not exist."
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    extension = Extensions.get({ "order_id": order_id, "res_dt_start": ext_dt_start })

    if extension is None:
        error = "This extension does not exist." 
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    status = safe_swap_items(extension, swap_item)
    response = make_response({ "message": status.message }, CODE_2_OK)
    return  response