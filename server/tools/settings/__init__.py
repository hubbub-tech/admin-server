from celery import Celery

from .config import Config, AWSConfig, MailConfig

from .utils import create_auth_token, verify_auth_token
from .utils import login_user, login_required
from .utils import json_sort, append_sort

from .const import *

AWS = AWSConfig.get_instance()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
