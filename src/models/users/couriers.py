from blubber_orm import Models

class Couriers(Models):

    table_name = "couriers"
    table_primaries = ["courier_id"]
    sensitive_attributes = ["courier_session_key"]

    def __init__(self, attrs: dict):
        self.courier_id = attrs["courier_id"]
        self.courier_session_key = attrs["courier_session_key"]
        self.is_admin = attrs["is_admin"]
