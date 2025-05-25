class Config:
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SERVER_NAME = "0.0.0.0"
    PORT = 4444
    SECRET_KEY = "5fc89e7726bab6cd0ce9502d09ae36bfd654a67a103829159fd8c9245510eb0d"


class DevelopmentConfig(Config):
    SECRET_KEY = "my_Secret_Key"
