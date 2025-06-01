from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.json.ensure_ascii = False
app.config.from_object("config.DevConfig")

db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow()
ma.init_app(app)


# DONE. Обязательно добавить импорт для обработчиков author и quote
from api.handlers import author
from api.handlers import quote