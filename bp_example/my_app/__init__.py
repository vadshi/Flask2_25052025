
from flask import Flask
from my_app.hello_as_bp.handlers import hello as hello_bp


def create_app(mode="dev"):
    app = Flask(__name__)
    app.register_blueprint(hello_bp)
    if mode == "dev":   
        app.config.from_object("my_app.config.DevelopmentConfig")
    elif mode == "prod":
        app.config.from_object("my_app.config.ProductionConfig")

    return app

    
