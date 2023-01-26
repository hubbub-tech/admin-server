from datetime import datetime

from src.models import Items
from src.models import Users
from src.models import Orders
from src.models import Logistics

from src.utils.settings import smtp_config

from ._email_table import EmailTable, EmailTableRow
from ._email_body import EmailBodyMessenger, EmailBodyFormatter


def get_time_sched_email(logistics: Logistics, dt_sched_eta: datetime):

    email_body_messenger = EmailBodyMessenger()
    email_body_formatter = EmailBodyFormatter()

    order_ids = logistics.get_order_ids()

    order = Orders.get({"id": order_ids[0] })
    renter = Users.get({"id": order.renter_id })

    email_body_formatter.preview = f"Your courier event time has been set for {dt_sched_eta.strftime('%I:%M:00 %p')}."

    email_body_formatter.user = renter.name

    email_body_formatter.introduction = f"""
        Thanks for submitting your availability! We have scheduled a specific time for your courier event. See the information 
        below for details.
        """

    table_rows = []
    for order_id in order_ids:
        
        order = Orders.get({"id": order_id })
        item = Items.get({"id": order.item_id })

        row_data = {
            "Item": item.name,
            "Start date": order.res_dt_start.strftime("%b %-d, %Y"),
            "End date": order.ext_dt_end.strftime("%b %-d, %Y")
        }

        table_row = EmailTableRow(row_data)
    table_rows.append(table_row)

    email_table = EmailTable(table_rows, title=f"Events scheduled for: {dt_sched_eta.strftime('%B %-d, %Y')}")
    email_body_formatter.optional = email_table.to_html()


    email_body_formatter.content = """
        You will receive a tracking link when the Hubbub courier is on their way.
        Our team will also be in touch through our number, (929) 244-0748, should any details change in your event.
        """

    email_body_formatter.conclusion = f"If you have any questions, please contact us at {smtp_config.DEFAULT_RECEIVER}."

    body = email_body_formatter.build()

    email_body_messenger.subject = f"[Hubbub] Confirming Your Event Time"
    email_body_messenger.to = (renter.email, smtp_config.DEFAULT_RECEIVER)
    email_body_messenger.body = body
    return email_body_messenger
