from .config import FlaskConfig, AWSConfig, SMTPConfig

from .const import *
from .codes import *

aws_config = AWSConfig.get_instance()
smtp_config = SMTPConfig.get_instance()