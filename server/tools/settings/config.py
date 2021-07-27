import os
import boto3

#SUPPORTING CONFIGS------------------------------

class AWSConfig:
    _instance = None
    S3_OBJECT = None
    S3_LINK = None
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None

    def __init__(self):
        if AWSConfig._instance:
            #TODO: log that this problem happened
            raise Exception("AWS Connection should only be created once in the app.")
        else:
            AWSConfig.S3_LINK = "https://{}.s3.amazonaws.com".format(os.environ['S3_BUCKET'])
            AWSConfig.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
            AWSConfig.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
            AWSConfig.S3_BUCKET = os.environ['S3_BUCKET']
            AWSConfig.set_s3()

            AWSConfig._instance = self

    @staticmethod
    def get_instance():
        if AWSConfig._instance is None:
            AWSConfig()
        return AWSConfig._instance

    @staticmethod
    def set_s3():
        if AWSConfig.S3_OBJECT is None:
            s3 = boto3.client(
                's3',
                aws_access_key_id=AWSConfig.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWSConfig.AWS_SECRET_ACCESS_KEY
            )
            AWSConfig.S3_OBJECT = s3

    @staticmethod
    def get_s3_resource():
        if AWSConfig._instance:
            s3_resource = boto3.resource("s3")
            return s3_resource
        else:
            raise Exception("An instance of the AWSConfig must be created before accessing s3.")

    @staticmethod
    def get_url(path):
        url = "/".join([AWSConfig.S3_LINK, path])
        return url

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
