import os

#FLASK CONFIGS------------------------------------

class Config:

    SECRET_KEY = os.environ['SECRET_KEY']
    TESTING = False

    #Celery
    OPERATIONS_APIKEY = os.environ['OPERATIONS_APIKEY']
    CORS_ALLOW_ORIGINS = {
        "admin": os.environ['ADMIN_CORS_ORIGIN'],
        "shop": os.environ['SHOP_CORS_ORIGIN']
    }
    CELERY_BROKER_URL = os.environ['CLOUDAMQP_URL']
    CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
    BROKER_POOL_LIMIT = 1
    #CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

    #Upload management
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
