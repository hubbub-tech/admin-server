from celery import Celery

from .config import FlaskConfig, AWSConfig, SMTPConfig

from .const import *
from .codes import *

aws_config = AWSConfig.get_instance()
smtp_config = SMTPConfig.get_instance()

celery = Celery(__name__, broker=FlaskConfig.CELERY_BROKER_URL)
