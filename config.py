import os

class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.getenv("SECRET_KEY", "m1n4ngs3d4p")

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True