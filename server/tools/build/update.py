from blubber_orm import Items, Orders, Addresses
from blubber_orm import Dropoffs, Pickups, Logistics

def complete_task(order, task):
    is_valid = False
    message = f"The task on order #{order.id} for the {item.name} has failed."
    if isinstance(task, Dropoffs):
        Dropoffs.mark_as_delivered(order)
    elif isinstance(task, Pickups):
        Pickups.mark_as_collected(order)
    else:
        raise Exception("The only valid task types are: 'Dropoffs' and 'Pickups'.")
    Items.set(order.item_id, {
        "address_num": task.logistics.address.num,
        "address_street": task.logistics.address.street,
        "address_apt": task.logistics.address.apt,
        "address_zip": task.logistics.address.zip_code
    })
    is_valid = True
    message = f"The task on order #{order.id} for the {item.name} has been completed."
    return {
        "is_valid": is_valid,
        "message": message
    }