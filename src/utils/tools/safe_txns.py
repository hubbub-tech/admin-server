from src.models import Reservations
from src.models import Extensions
from src.models import Orders
from src.models import Items
from src.models import Users

from src.utils.classes import Status

from .factories import create_reservation

def safe_swap_items(txn, item: Items):
    assert txn.table_name in ["orders", "extensions"]
    assert isinstance(item, Items)

    renter = Users.get({ "id": txn.renter_id })

    status = Status()
    if item.is_locked == False:
        item.lock(renter)

        txn_reservation = Reservations.get({
            "item_id": txn.item_id,
            "renter_id": txn.renter_id,
            "dt_started": txn.res_dt_start,
            "dt_ended": txn.res_dt_end,
        })

        copy_reservation_to_dict = txn_reservation.to_dict()
        copy_reservation_to_dict["item_id"] = item.id

        Reservations.set({
            "item_id": txn.item_id,
            "renter_id": txn.renter_id,
            "dt_started": txn.res_dt_start,
            "dt_ended": txn.res_dt_end,
        }, { "is_calendered": False })

        swapped_reservation = create_reservation(copy_reservation_to_dict)

        if isinstance(txn, Orders):
            Orders.set({ "id": txn.id }, { "item_id": swapped_reservation.item_id })
        elif isinstance(txn, Extensions):
            Extensions.set({ 
                "order_id": txn.order_id, 
                "res_dt_start": swapped_reservation.dt_started 
            }, { "item_id": swapped_reservation.item_id })

        item.unlock()
        status.is_successful = True
        status.message = f"The item (id:{txn_reservation.item_id}) was successfully swapped for item (id:{item.id})."
        return status

    else:
        status.is_successful = False
        status.message = "Sorry, it seems like someone else is transacting on this item. Try again in a few minutes."
        return status