import boto3
from datetime import datetime, date, timedelta
from botocore.exceptions import NoCredentialsError
from werkzeug.security import check_password_hash, generate_password_hash
from blubber_orm import Users

from server.tools.settings import AWS

def validate_login(form_data):
    is_valid = False
    loaded_user = Users.filter({"email": form_data["email"]})
    if loaded_user:
        loaded_user, = loaded_user
        if not check_password_hash(loaded_user.password, form_data["password"]):
            message = "Sorry, invalid password and email combination."
        elif not loaded_user.is_courier:
            message = "Sorry, you're not authorized to be a courier at the moment."
        else:
            is_valid = True
            message = "You logged in, welcome back!"
    else:
        message = "Sorry, invalid password and email combination."
    return {
        "is_valid" : is_valid,
        "message" : message
        }
