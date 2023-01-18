from src.models import Users
from src.models import Items
from src.models import Calendars
from src.models import Addresses
from src.models import Logistics
from src.models import Reservations
from src.models import Orders
from src.models import Extensions

from src.utils.classes import PriceCalculator
from src.utils.settings import DEPOSIT, TAX, DISCOUNT


def create_address(insert_data: dict):
    address = Addresses.get({
        "lat": insert_data["lat"],
        "lng": insert_data["lng"]
    })
    if address is None:
        address = Addresses.insert(insert_data)

    return address


def create_reservation(insert_data: dict, strict_mode: bool=False):
    if insert_data["dt_started"] >= insert_data["dt_ended"]: return

    item = Items.get({"id": insert_data["item_id"]})
    reservation = Reservations.unique(insert_data)

    if strict_mode:
        reservation = Reservations.insert(insert_data)
        return reservation

    if reservation is None:
        dt_ended = insert_data["dt_ended"]
        dt_started = insert_data["dt_started"]
        duration = (dt_ended - dt_started).days

        price_calculator = PriceCalculator()
        insert_data["est_charge"] = price_calculator.get_rental_cost(item.retail_price, duration)
        insert_data["est_deposit"] = insert_data["est_charge"] * DEPOSIT
        insert_data["est_tax"] = insert_data["est_charge"] * TAX

        reservation = Reservations.insert(insert_data)

    return reservation

def create_extension(insert_data: dict):
    reservation_keys = {
        "dt_started": insert_data["res_dt_start"],
        "dt_ended": insert_data["res_dt_end"],
        "renter_id": insert_data["renter_id"],
        "item_id": insert_data["item_id"]
    }

    Reservations.set(reservation_keys, {"is_extension": True})
    new_extension = Extensions.insert(insert_data)

    return new_extension


def create_order(insert_data: dict):
    new_order = Orders.insert(insert_data)

    renter = Users.get({ "id": new_order.renter_id })
    return new_order


def create_logistics(insert_data: dict):
    logistics = Logistics.unique(insert_data)
    if logistics is None:
        receiver = Users.get({ "id": insert_data["receiver_id"] })
        sender = Users.get({ "id": insert_data["sender_id"] })

        receiver.add_role(role="receivers")
        sender.add_role(role="senders")

        logistics = Logistics.insert(insert_data)
    print(logistics)
    return logistics


def create_charge(insert_data: dict):
    return None
