import json
import pytz
import string
import random
import functools
from datetime import datetime
from flask import session, request, flash, g, make_response
from blubber_orm import Users
from werkzeug.security import check_password_hash, generate_password_hash

from .config import Config
from .const import COOKIE_KEY_SESSION, COOKIE_KEY_USER

# NOTE: ONLY COMPATIBLE WITH POST METHOD ROUTES****
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if request.method == 'POST':
            if request.json: data = request.json
            elif request.form: data = request.form
            else: return {"flashes": "No data was sent, try again."}, 403

            session = data.get(COOKIE_KEY_SESSION)
            user_id = data.get(COOKIE_KEY_USER)
        else:
            session = request.cookies.get(COOKIE_KEY_SESSION)
            user_id = request.cookies.get(COOKIE_KEY_USER)

        is_authenticated = verify_auth_token(session, user_id)
        if is_authenticated:
            g.user_id = int(user_id)
            g.user = Users.get(user_id)
            return view(**kwargs)
        else:
            data = {"flashes": ["Your login session has ended. Login again."]}
            response = make_response(data, 403)
            return response
    return wrapped_view

def login_user(user):
    is_valid = True
    if user.is_blocked:
        is_valid = False
        message = "The admin has decided to block your account. Contact hubbubcu@gmail.com for more info."
    else:
        session.clear()
        session["user_id"] = user.id
        message = "You're logged into the courier app, welcome back!"
    return {
        "is_valid" : is_valid,
        "message" : message
        }

def create_auth_token(user):
    letters = string.ascii_letters
    new_session = ''.join(random.choice(letters) for i in range(10))
    user.session = new_session
    hashed_token = generate_password_hash(new_session)
    return hashed_token

def verify_auth_token(hashed_token, user_id):
    if user_id and hashed_token:
        user = Users.get(user_id)
        if user.session:
            return check_password_hash(hashed_token, user.session)
    return False

def append_sort(arr, element, key):
    """element should be type dictionary containing the passed key"""
    if len(arr) == 0:
        arr.append(element)
    else:
        i = 0
        while i < len(arr):
            if arr[i][key] >= element[key]:
                arr.insert(i, element)
                break
            elif i == len(arr) - 1:
                arr.append(element)
                break
            i += 1

def json_sort(arr, key, reverse=False):
    """Takes an array of dictionaries with the same structure and sorts"""
    arr.sort(key = lambda element: element[key], reverse=reverse)
