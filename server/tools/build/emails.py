from datetime import datetime, date, timedelta

def get_task_time_email(task, chosen_time):
    frame_data = {}
    frame_data["preview"] = f"Your {task['type']} time has been set for {chosen_time.strftime('%I:%M:00 %p')} - "
    frame_data["user"] = task["renter"]["name"]
    frame_data["introduction"] = f"""
        Thanks for scheduling your {task['type']}! We have scheduled a specific time
        for your rental. See the table below.
        """
    frame_data["content"] = get_task_update_table(task, chosen_time)
    if task['type'] == "pickup":
        clause = """
            Also, please make sure each item is in a clean and usable state upon
            pick-up, charges may be applied otherwise.
            """
    else:
        total_tax = 0
        total_deposit = 0
        total_charge = 0
        for order in task["orders"]:
            reservation = order["reservation"]
            total_tax += reservation["tax"]
            total_deposit += reservation["deposit"]
            total_charge += reservation["charge"]
        total = total_tax + total_deposit + total_charge
        clause = "Upon dropoff, you will be charged a total of ${:,.2f}. The breakdown: ".format(total)
        clause += "Tax: ${:,.2f}, ".format(total_tax) + "Deposit: ${:,.2f}, ".format(total_deposit) + "Cost: ${:,.2f}.".format(total_charge)
    frame_data["conclusion"] = f"""
        Please be prompt, as a $5 {task['type']} attempt charge will be made if you do not show
        up after 30 minutes. {clause}
        """
    email_data = {}
    email_data["subject"] = f"[Hubbub] Confirming your {task['type']} time"
    email_data["to"] = (task['renter']['email'], "hubbubcu@gmail.com")
    email_data["body"] = email_builder(frame_data)
    email_data["error"] = "TASK-TIME"
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

def get_task_update_table(task, chosen_time):
    task_date = datetime.strptime(task["task_date"], "%Y-%m-%d").date()
    task_date_str = datetime.strftime(task_date, "%B %-d, %Y")

    item_links =[]
    items = [order["item"] for order in task["orders"]]
    for item in items:
        item_links.append(f"<a href='https://www.hubbub.shop/inventory/i/id={item['id']}'>{item['name']}</a>")

    item_names = ", ".join(item_links)
    task_table = f"""
        <table>
            <tr>
                <th>Name</th>
                <th>Details</th>
            </tr>
            <tr>
                <td>Date for {task['type']}</td>
                <td>{task_date_str}</td>
            </tr>
            <tr>
                <td>Chosen time</td>
                <td>{chosen_time.strftime('%I:%M:00 %p')}</td>
            </tr>
            <tr>
                <td>Item(s)</td>
                <td>{item_names}</td>
            </tr>
        </table>
        <p>
        Address for {task['type']}: {task['address']['num']} {task['address']['street']},
        {task['address']['city']} {task['address']['state']}, {task['address']['zip_code']}
        </p>
        """
    return task_table
