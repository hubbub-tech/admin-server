from src.models import Users

from .emails import get_sunset_email

class Agent:

    def __init__(self):
        pass


    @staticmethod
    def write_sunset_email(user_id):

        try: 
            user = Users.get({ "id": user_id })
        except: 
            return None
        else: 
            if user:
                email_data = get_sunset_email(user)
                return email_data
            else:
                return None
