import os

from decouple import config


class Config:
    SECRET_KEY= config('SECRET_KEY')
    DEBUG = False
    TESTING = False

    # AWS
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

class DevelopmentConfig(Config):
    DEBUG = True
    S3_BUCKET_NAME = "mi-bucket-develop" 
    UPLOAD_TO_S3 = False

class ProductionConfig(Config):
    S3_BUCKET_NAME = "mi-bucket-produccion"
    UPLOAD_TO_S3 = True

configuration = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
