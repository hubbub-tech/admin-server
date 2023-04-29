from src.utils import upload_email_data
from src.utils import Agent

agent = Agent()

if __name__ == "__main__":
    
    for user_id in range(4000):
        email_data = agent.write_sunset_email(user_id)
        if email_data:
            upload_email_data(email_data, email_type='sunset_notice')