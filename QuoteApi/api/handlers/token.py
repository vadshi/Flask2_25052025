from flask import jsonify
from api import app, db, basic_auth
from api.models.user import UserModel
from api.schemas.token import TokenOut

@app.route('/auth/token')
@app.auth_required(basic_auth)
@app.output(TokenOut, status_code=201)
def get_auth_token():
    """ Получаем токен по имени и паролю"""
    username = basic_auth.current_user
    user = db.one_or_404(db.select(UserModel).filter_by(username=username))
    token = user.generate_auth_token()
    return {"token": token}
