import os
from flask import Blueprint, g, request
from flask_cors import CORS
from blubber_orm import Orders, Users, Reservations
from blubber_orm import Items, Details, Calendars
from blubber_orm import Dropoffs, Pickups

from server.tools.settings import Config, AWS
from server.tools.settings import json_sort

bp = Blueprint('manage_items', __name__)
CORS(bp, origins=[Config.CORS_ALLOW_ORIGINS["admin"]])

@bp.get("/item/history/id=<int:item_id>")
def item_history(item_id):
    photo_url = AWS.get_url("items")
    item = Items.get(item_id)
    lister = Users.get(item.lister_id)
    item_to_dict = item.to_dict()
    item_to_dict["lister"] = lister.to_dict()
    item_to_dict["lister"]["name"] = lister.name
    next_start, next_end = item.calendar.next_availability()
    item_to_dict["address"] = item.address.to_dict()
    item_to_dict["details"] = item.details.to_dict()
    item_to_dict["calendar"] = item.calendar.to_dict()
    item_to_dict["calendar"]["next_available_start"] = next_start.strftime("%Y-%m-%d")
    item_to_dict["calendar"]["next_available_end"] = next_end.strftime("%Y-%m-%d")
    db_orders = Orders.filter({ "item_id": item.id })
    orders = []
    for order in db_orders:
        renter = Users.get(order.renter_id)
        order_to_dict = order.to_dict()
        order_to_dict["renter"] = renter.to_dict()
        order_to_dict["renter"]["name"] = renter.name
        order_to_dict["reservation"] = order.reservation.to_dict()
        order_to_dict["ext_date_end"] = order.ext_date_end.strftime("%Y-%m-%d")
        orders.append(order_to_dict)
    item_to_dict["orders"] = orders
    return {
        "item": item_to_dict,
        "photo_url": photo_url
    }

@bp.post("/item/hide/id=<int:item_id>")
def hide_item(item_id):
    code = 406
    flashes = []
    item = Items.get(item_id)
    data = request.json
    if data:
        item.is_available = data["toggle"]
        if item.is_available:
            flashes.append("Item has been revealed. Others can now see it in inventory.")
        else:
            flashes.append("Item has been hidden. Come back when you are ready to reveal it.")
        code = 201
    else:
        flashes.append("No data was sent! Try again.")
    return {"flashes": flashes}, code

@bp.post("/item/feature/id=<int:item_id>")
def feature_item(item_id):
    code = 406
    flashes = []
    item = Items.get(item_id)
    data = request.json
    if data:
        item.is_featured = data["toggle"]
        if item.is_featured:
            flashes.append("Item has been featured. It has risen to the top of the inventory page on shop.")
        else:
            flashes.append("Item has been unfeatured. Come back when you are ready to feature it again.")
        code = 201
    else:
        flashes.append("No data was sent! Try again.")
    return {"flashes": flashes}, code

@bp.post("/item/edit/id=<int:item_id>/submit")
def edit_item_submit(item_id):
    flashes = []
    data = request.form
    if data:
        # date_end_extended = json_date_to_python_date(data["extendEndDate"])
        form_data = {
            "price": data["price"],
            "description": data["description"],
            # "extend": date_end_extended
        }
        Items.set(item.id, {"price": form_data["price"]})
        Details.set(item.id, {"description": form_data["description"]})
        # Calendars.set(item.id, {"date_ended": date_end_extended})
        image = request.files.get("image", None)
        if image:
            image_data = {
                "self" : item,
                "image" : image,
                "directory" : "items",
                "bucket" : AWS.S3_BUCKET
            }
            upload_response = upload_image(image_data)
            flashes.append(upload_response["message"])
        flashes.append(f"Your {item.name} has been updated!")
        code = 201
    else:
        flashes.append("No changes were received! Try again.")
        code = 406
    return {"flashes": flashes}, code

@bp.post("/item/address/id=<int:item_id>/submit")
def edit_item_address_submit(item_id):
    flashes = []
    data = request.json
    if data:
        form_data = {
            "num": data["address"]["num"],
            "street": data["address"]["street"],
            "apt": data["address"].get("apt", ""),
            "zip": data["address"]["zip"],
            "city": data["address"]["city"],
            "state": data["address"]["state"]
        }
        new_address = Addresses.filter(form_data)
        if not new_address:
            new_address = Addresses.insert(form_data)
        Items.set(item_id, {
            "address_num": form_data["num"],
            "address_street": form_data["street"],
            "address_apt": form_data["apt"],
            "address_zip": form_data["zip"]
        })
        flashes.append("You successfully changed your address!")
        return {"flashes": flashes}, 201
    else:
        flashes.append("No data was sent! Try again.")
    return {"flashes": flashes}, 201
