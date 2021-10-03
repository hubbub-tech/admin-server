from blubber_orm import Orders, Users, Items
from datetime import datetime, date, timedelta

def get_pickup_schedule_reminder(renter, orders):
    frame_data = {}
    frame_data["preview"] = f"Remember to schedule a pickup for your rental(s) - "
    frame_data["user"] = renter.name
    frame_data["introduction"] = f"""
        Hey there! It seems like you still have {len(orders)} rental(s) without
        pickups scheduled. Your rental(s) have been listed below:
        """
    frame_data["content"] = get_active_orders_table(orders)
    frame_data["conclusion"] = f"""
        You can schedule your pickup at <a href="https://www.hubbub.shop/accounts/u/orders">My Rentals</a>.
        Alternatively, you can extend your rental for any of these items by following the same link.
        """
    email_data = {}
    email_data["subject"] = f"[Hubbub] Remember to Schedule your Pickup(s)!"
    email_data["to"] = (renter.email, "hubbubcu@gmail.com")
    email_data["body"] = email_builder(frame_data)
    email_data["error"] = "REMINDER-PICKUP"
    return email_data

def get_task_time_email(task, chosen_time):
    frame_data = {}
    frame_data["preview"] = f"Your {task['type']} time has been set for {chosen_time.strftime('%I:%M:00 %p')} - "
    frame_data["user"] = task["renter"]["name"]
    frame_data["introduction"] = f"""
        Thanks for submitting your availability! We have scheduled a specific time
        for your {task['type']}. See the information below for details.
        """
    frame_data["content"] = get_task_update_table(task, chosen_time)

    total_tax = 0
    total_deposit = 0
    total_charge = 0
    for order in task["orders"]:
        reservation = order["reservation"]
        total_tax += reservation["tax"]
        total_deposit += reservation["deposit"]
        total_charge += reservation["charge"]
    if task['type'] == "pickup":
        charge = "" #"Your deposit will be returned at pickup."
        clause = """
            Please make sure each item is in a clean and usable state upon pickup,
            charges may be applied otherwise.
            """
    else:
        total = round(total_tax + total_deposit + total_charge, 2)
        charge = f"Total due at dropoff: ${total}"
        clause = ""
    frame_data["conclusion"] = f"""
            {charge}
        </p>
        <p>
            We will be sending you a text from our Hubbub phone number (929) 244-0748‬ when we are on
            our way to you. Feel free to text or call us at that number with any updates or changes
            on the day of {task['type']}.
        </p>
        <p>
            Please be prompt, as a $5 {task['type']} attempt charge will be made if you do not show
            up after 30 minutes. {clause}
        </p>
        <p>
            Let us know if anything looks incorrect with the above information or if you have any questions!
        """
    email_data = {}
    email_data["subject"] = f"[Hubbub] Confirming your {task['type'].capitalize()} Time"
    email_data["to"] = (task['renter']['email'], "hubbubcu@gmail.com")
    email_data["body"] = email_builder(frame_data)
    email_data["error"] = "TASK-TIME"
    return email_data

def update_task_time_email(task, chosen_time):
    frame_data = {}
    frame_data["preview"] = f"Your {task['type']} time has been updated to {chosen_time.strftime('%I:%M:00 %p')} - "
    frame_data["user"] = task["renter"]["name"]
    frame_data["introduction"] = f"""
        We have updated your {task['type']} time. See the information below for details.
        """
    frame_data["content"] = get_task_update_table(task, chosen_time)

    total_tax = 0
    total_deposit = 0
    total_charge = 0
    for order in task["orders"]:
        reservation = order["reservation"]
        total_tax += reservation["tax"]
        total_deposit += reservation["deposit"]
        total_charge += reservation["charge"]
    if task['type'] == "pickup":
        charge = "" #"Your deposit will be returned at pickup."
        clause = """
            Please make sure each item is in a clean and usable state upon pickup,
            charges may be applied otherwise.
            """
    else:
        total = round(total_tax + total_deposit + total_charge, 2)
        charge = f"Total due at dropoff: ${total}"
        clause = ""
    frame_data["conclusion"] = f"""
            {charge}
        </p>
        <p>
            We will be sending you a text from our Hubbub phone number (929) 244-0748‬ when we are on
            our way to you. Feel free to text or call us at that number with any updates or changes
            on the day of {task['type']}.
        </p>
        <p>
            Please be prompt, as a $5 {task['type']} attempt charge will be made if you do not show
            up after 30 minutes. {clause}
        </p>
        <p>
            Let us know if anything looks incorrect with the above information or if you have any questions!
        """
    email_data = {}
    email_data["subject"] = f"[Hubbub] Updating your {task['type'].capitalize()} Time"
    email_data["to"] = (task['renter']['email'], "hubbubcu@gmail.com")
    email_data["body"] = email_builder(frame_data)
    email_data["error"] = "TASK-TIME"
    return email_data

def get_task_confirmation_email(task, address):
    task_date = datetime.strptime(task["task_date"], "%Y-%m-%d").date()
    task_date_str = datetime.strftime(task_date, "%B %-d, %Y")
    item_names = get_linkable_items(task)

    address_formatted = f"{address['num']} {address['street']}, {address['city']} {address['state']}, {address['zip_code']}"
    frame_data = {}
    frame_data["preview"] = f"Your {task['type']} has been marked as completed! See this email for verification - "
    frame_data["user"] = task["renter"]["name"]

    if task['type'] == 'dropoff':
        intro = f"""
            This email is to confirm that your rental(s) beginning on {task_date_str}
            has been dropped off at <strong>{address_formatted}</strong>.
            """
        action = "receive"
    else:
        intro = f"""
            This email is to confirm that your rental(s) ending on {task_date_str}
            has been picked up.
            """
        action = "return"
    frame_data["introduction"] = intro
    frame_data["content"] = f"""
        <p>
            The item(s) in this rental order were: {item_names}
        </p>
        """

    frame_data["conclusion"] = f"""
            If you or someone you authorized did not {action} the above item(s),
            please contact us immediately at (929) 244-0748‬ or reply to this email.
            Otherwise, no action is needed.
        </p>
        <p>
            Please let us know if you ever need anything else!
        """

    email_data = {}
    email_data["subject"] = f"[Hubbub] Your {task['type'].capitalize()} has been Completed!"
    email_data["to"] = (task['renter']['email'], "hubbubcu@gmail.com")
    email_data["body"] = email_builder(frame_data)
    email_data["error"] = "TASK-COMPLETED"
    return email_data

#EMAIL HELPERS---------------------------------------

def email_builder(frame_data):
    frame = """
        <!doctype html>
        <html lang="en">
          <head>
            <style>
              .preheader {{
                color: transparent;
                display: none;
                height: 0;
                max-height: 0;
                max-width: 0;
                opacity: 0;
                overflow: hidden;
                mso-hide: all;
                visibility: hidden;
                width: 0;
                }}
              td, th {{
                border: 1px solid #ffffff;
                text-align: left;
                padding: 8px;
                }}
              div.content {{
                  width: 600px;
                  margin: 0em 5em 5em 5em;
                  padding: 2em;
                  background-color: #fdfdff;
                  border-radius: 0em 0em 0.5em 0.5em;
                  box-shadow: 0px 3px 7px 2px rgba(0,0,0,0.02);
                  }}
            </style>
          </head>
          <body style="background-color: #f0f0f2; font-family: arial, sans-serif; margin: 0; padding: 0;">
            <span class="preheader">{preview}</span>
            <div class="content">

              <!-- START CENTERED WHITE CONTAINER -->
              <table role="presentation" class="main">

                <!-- START MAIN CONTENT AREA -->
                <tr>
                  <p>Hi {user},</p>
                  <p>{introduction}</p>
                </tr>
                <tr>
                  {content}
                </tr>
                <tr>
                    <br>
                  <p>{conclusion}</p>
                  <p>Sincerely,</p>
                  <p>  Team Hubbub</p>
                </tr>
              </table>
              <!-- END CENTERED WHITE CONTAINER -->

              <!-- START FOOTER-->
              <div class="footer">
                <small>
                  <span>Hubbub HQ, 523 W. 160th St., Apt 5A, New York, NY 10032</span>
                  <br> Continue shopping at <a href="https://www.hubbub.shop/inventory">Hubbub Shop</a>.
                <small>
              </div>
              <!--END FOOTER -->

            </div>
          </body>
        </html>
        """.format(
                preview=frame_data["preview"],
                user=frame_data["user"],
                introduction=frame_data["introduction"],
                content=frame_data["content"],
                conclusion=frame_data["conclusion"]
                )
    return frame

def get_active_orders_table(orders):
    active_orders_table = f"""
        <table>
            <tr>
                <th>Item</th>
                <th>End Date</th>
            </tr>
        """
    for order in orders:
        item = Items.get(order.item_id)
        link = f"https://www.hubbub.shop/inventory/i/id={item.id}"
        order_end_date_str = datetime.strftime(order.ext_date_end, "%B %-d, %Y")
        row = f"""
            <tr>
                <td><a href='{link}'>{item.name}</a></td>
                <td>{order_end_date_str}</td>
            </tr>
            """
        active_orders_table += row
    active_orders_table += "</table>"
    return active_orders_table

def get_task_update_table(task, chosen_time):
    task_date = datetime.strptime(task["task_date"], "%Y-%m-%d").date()
    task_date_str = datetime.strftime(task_date, "%B %-d, %Y")

    item_names = get_linkable_items(task)

    task_table = f"""
        <table>
            <tr>
                <td>{task['type'].capitalize()} Date</td>
                <td>{task_date_str}</td>
            </tr>
            <tr>
                <td>{task['type'].capitalize()} Time</td>
                <td>{chosen_time.strftime('%-I:%M %p')}</td>
            </tr>
            <tr>
                <td>{task['type'].capitalize()} Address</td>
                <td>{task['address']['num']} {task['address']['street']}, {task['address']['city']} {task['address']['state']}, {task['address']['zip_code']}</td>
            </tr>
            <tr>
                <td>Item(s)</td>
                <td>{item_names}</td>
            </tr>
        </table>
        """
    return task_table

def get_linkable_items(task):
    item_links =[]
    items = [order["item"] for order in task["orders"]]
    for item in items:
        link = f"https://www.hubbub.shop/inventory/i/id={item['id']}"
        item_links.append(f"<a href='{link}'>{item['name']}</a>")
    item_names = ", ".join(item_links)
    return item_names
