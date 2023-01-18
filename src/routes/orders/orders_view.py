from flask import Blueprint, g, request, make_response

from src.models import Extensions
from src.models import Orders
from src.models import Users
from src.models import Items

from src.utils import login_required

from src.utils.settings import (
    CODE_2_OK,
    CODE_4_NOT_FOUND
)

bp = Blueprint('view', __name__)

@bp.get("/order/<int:order_id>")
@login_required
def view_order(order_id):
    order = Orders.get({ "id": order_id })

    if order is None:
        error = "This order does not exist." 
        response = make_response({ "message": error }, CODE_4_NOT_FOUND)
        return response

    order_to_dict = order.to_dict()

    order_to_dict["ext_dt_start"] = order.ext_dt_start
    order_to_dict["ext_dt_end"] = order.ext_dt_end

    order_to_dict["total_charge"] = order.get_total_charge()
    order_to_dict["total_deposit"] = order.get_total_deposit()
    order_to_dict["total_tax"] = order.get_total_tax()

    order_to_dict["dropoff_id"] = order.get_dropoff_id()
    order_to_dict["pickup_id"] = order.get_pickup_id()

    item = Items.get({ "id": order.item_id })
    renter = Users.get({ "id": order.renter_id })

    order_to_dict["item_name"] = item.name
    order_to_dict["renter_name"] = renter.name

    extension_pkeys = order.get_extensions()

    extensions = []
    for ext_pkey_tuple in extension_pkeys:
        order_id_index = 0
        order_id = ext_pkey_tuple[order_id_index]

        res_dt_start_index = 3
        res_dt_start = ext_pkey_tuple[res_dt_start_index]

        extension = Extensions.get({ "order_id": order_id, "res_dt_start": res_dt_start })
        extension_to_dict = extension.to_dict()
        extensions.append(extension_to_dict)

    data = { "order": order_to_dict, "extensions": extensions }

    response = make_response(data, CODE_2_OK)
    return response