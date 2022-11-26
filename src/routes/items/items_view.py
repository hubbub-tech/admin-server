from flask import Blueprint, make_response, request

from src.models import Items

bp = Blueprint("view", __name__)

@bp.get("/item/<int:item_id>")
@login_required
def view_item(item_id):
