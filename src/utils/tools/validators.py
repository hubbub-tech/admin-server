from werkzeug.security import check_password_hash

from src.models import Users

from src.utils.classes import Status


def validate_login(form_data):
    loaded_user = Users.unique({"email": form_data["email"]})

    status = Status()
    if loaded_user is None:
        status.message = "Could not find this user."
        status.is_successful = False
        return status

    if not check_password_hash(loaded_user.password, form_data["password"]):
        status.message = "Sorry, invalid password and email combination."
        status.is_successful = False
        return status

    status.message = "Successful email and password match!"
    status.is_successful = True
    return status
