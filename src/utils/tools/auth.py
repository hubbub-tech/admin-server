import string
import random

from werkzeug.security import generate_password_hash, check_password_hash

from src.models import Couriers, Users

from src.utils.classes import Status


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        courier_id = request.cookies.get("courierId")
        courier_session_key_hashed = request.cookies.get("courierSessionToken")

        if courier_id:
            courier = Couriers.get({"courier_id": courier_id })
            if user:
                is_authorized = verify_token(courier_session_key_hashed, courier.courier_session_key)
            else:
                is_authorized = False
        else:
            is_authorized = False

        if is_authorized == False:
            error = "Login first to continue using this page."
            response = make_response({ "message": error }, 403)
            return response

        g.courier_id = courier.courier_id
        g.courier_session_key = courier.courier_session_key

        return view(**kwargs)
    return wrapped_view


def login_courier(courier: Couriers):
    assert isinstance(courier, Couriers)

    status = Status()

    user = Users.get({ "id": courier.courier_id })

    if user.is_blocked:
        status.is_successful = False
        status.message = "Sorry, your account has been blocked. Contact us at hello@hubbub.shop if this seems wrong."
    else:
        status.is_successful = True
        status.message = "Welcome back!"
    return status


def gen_token():
    letters = string.ascii_letters
    unhashed_token = ''.join(random.choice(letters) for i in range(10))
    hashed_token = generate_password_hash(unhashed_token)
    return { "hashed": hashed_token, "unhashed": unhashed_token }


def verify_token(hashed_token, unhashed_token):
    return check_password_hash(hashed_token, unhashed_token)
