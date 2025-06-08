from flask import abort, jsonify, request
from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.schemas.user import user_schema


# url: /users/<int:user_id> - GET
@app.get("/users/<int:user_id>")
def get_user_by_id(user_id: int):
    user = db.get_or_404(UserModel, user_id, description=f"User with id={user_id} not found")
    return jsonify(user_schema.dump(user)), 200


# url: /users - GET
@app.get("/users")
def get_users():
    users = db.session.scalars(db.select(UserModel)).all()
    return jsonify(user_schema.dump(users, many=True)), 200



# url:  /users - POST
@app.post("/users")
def create_user():
    try:
        user = user_schema.loads(request.data)
        user.save()
    except ValidationError as ve:
        abort(400, f"Validation error: {ve.messages_dict}")
    
    return jsonify(user_schema.dump(user)), 201