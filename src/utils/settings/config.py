import os
import boto3

#SUPPORTING CONFIGS------------------------------

class AWSConfig:
    _instance = None
    S3_OBJECT = None

    def __init__(self):
        if AWSConfig._instance:
            #TODO: log that this problem happened
            raise Exception("AWS Connection should only be created once in the app.")
        else:
            self.S3_BUCKET = os.getenv('AWS_S3_BUCKET')
            self.S3_BASE_URL = f"https://{self.S3_BUCKET}.s3.amazonaws.com"

            self.ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
            self.SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

            AWSConfig._instance = self


    @staticmethod
    def get_instance():
        if AWSConfig._instance is None:
            AWSConfig()
        return AWSConfig._instance


    def get_base_url(self, bucket=None):
        if bucket:
            return f"https://{bucket}.s3.amazonaws.com"
        return self.S3_BASE_URL


    def get_s3(self):
        if AWSConfig.S3_OBJECT is None:
            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=self.ACCESS_KEY_ID,
                    aws_secret_access_key=self.SECRET_ACCESS_KEY
                )
            except Exception as e:
                raise Exception(e)
        else:
            s3 = AWSConfig.S3_OBJECT
        return s3


    @staticmethod
    def get_s3_resource():
        if AWSConfig._instance:
            s3_resource = boto3.resource("s3")
            return s3_resource
        else:
            raise Exception("An instance of the AWSConfig must be created before accessing s3.")


class SMTPConfig:
    _instance = None
    DEFAULT_SENDER = None
    DEFAULT_SENDER_PASSWORD = None
    SMTP_SERVER = ''
    SMTP_PORT = None

    def __init__(self):
        if SMTPConfig._instance:
            #TODO: log that this problem happened
            raise Exception("MAIL CLIENT Connection should only be created once in the app.")
        else:
            SMTPConfig.DEFAULT_ADMIN = os.getenv("MAIL_DEFAULT_ADMIN")
            SMTPConfig.DEFAULT_RECEIVER = os.getenv("MAIL_DEFAULT_RECEIVER")
            SMTPConfig.DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
            SMTPConfig.DEFAULT_SENDER_PASSWORD = os.getenv("MAIL_DEFAULT_SENDER_PASSWORD")
            SMTPConfig.SMTP_SERVER = os.getenv("SMTP_SERVER")
            SMTPConfig.SMTP_PORT = int(os.getenv("SMTP_PORT"))
            SMTPConfig._instance = self

    @staticmethod
    def get_instance():
        if SMTPConfig._instance is None:
            SMTPConfig()
        return SMTPConfig._instance

#FLASK CONFIGS------------------------------------

class FlaskConfig:

    SECRET_KEY = os.getenv('SECRET_KEY')
    TESTING = False

    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_ORIGIN = os.getenv('CORS_ALLOW_ORIGIN')


class DevelopmentFlaskConfig:

    SECRET_KEY = os.getenv('SECRET_KEY')
    TESTING = False

    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_ORIGIN = os.getenv('CORS_ALLOW_ORIGIN')


class TestFlaskConfig:

    SECRET_KEY = 'dev'
    TESTING = True

    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_ORIGIN = 'http://localhost:3000'

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
