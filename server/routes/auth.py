
from flask import Blueprint, g, request, make_response
from flask_cors import CORS

from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash

from blubber_orm import Users
from server.tools.settings import login_user, COOKIE_KEY_USER, COOKIE_KEY_SESSION
from server.tools.settings import create_auth_token, verify_auth_token
from server.tools.settings import Config

from server.tools.build import validate_login

bp = Blueprint('auth', __name__)
CORS(bp,
    origins=[Config.CORS_ALLOW_ORIGINS["admin"]],
    supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS
)

@bp.post('/login')
def login():
    flashes = []
    errors = []
    data = request.json
    if data:
        form_data = {
            "email": data["user"]["email"].lower(),
            "password": data["user"]["password"]
        }
        form_check = validate_login(form_data)
        if form_check["is_valid"]:
            user, = Users.filter({"email": form_data["email"]})
            login_response = login_user(user)
            if login_response["is_valid"]:
                session = create_auth_token(user)
                flashes.append(login_response["message"])
                data = {
                    "flashes": flashes,
                    COOKIE_KEY_USER: f'{user.id}',
                    COOKIE_KEY_SESSION: session
                }
                response = make_response(data, 200)
                return response
            else:
                errors.append(login_response["message"])
        else:
            errors.append(form_check["message"])
        flashes.append("Houston, we have a problem...")
    else:
        flashes.append("Nothing was entered! We need input to log you in.")
    data = {"errors": errors, "flashes": flashes}
    response = make_response(data, 401)
    return response
