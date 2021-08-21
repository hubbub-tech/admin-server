from celery import Celery

from .config import Config, AWSConfig, MailConfig

from .utils import json_sort, append_sort

AWS = AWSConfig.get_instance()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
