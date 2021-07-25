import json
import functools
from werkzeug.security import check_password_hash, generate_password_hash

from .config import Config

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
