import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from server.tools.settings import celery, MailConfig

@celery.task
def send_async_email(subject, to, body, error=None):
    MAIL = MailConfig.get_instance()
    msg = Mail(
        from_email=MAIL.DEFAULT_SENDER,
        to_emails=to,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(MAIL.SENDGRID_API_KEY)
        response = sg.send(msg)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
