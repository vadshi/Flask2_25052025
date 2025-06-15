from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
# from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from apiflask import APIFlask, HTTPBasicAuth, HTTPTokenAuth

class Base(DeclarativeBase):
    pass


app = APIFlask(__name__, title="Quote API", version="1.0")
app.tags = ["Quotes and Authors"]
app.json.ensure_ascii = False
app.config.from_object("config.DevConfig")

db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow()
ma.init_app(app)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme="Bearer")
# multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user = db.one_or_404(db.select(UserModel).filter_by(username=username))
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    from api.models.user import UserModel
    user = UserModel.verify_auth_token(token)
    return user


# DONE. Обязательно добавить импорт для обработчиков author и quote
from api.handlers import author
from api.handlers import quote
from api.handlers import user
from api.handlers import token