from flask import jsonify
from api import app, db, basic_auth
from api.models.user import UserModel


@app.route('/auth/token')
# @multi_auth.login_required
@app.auth_required(basic_auth)
def get_auth_token():
    username = basic_auth.current_user
    user = db.one_or_404(db.select(UserModel).filter_by(username=username))
    token = user.generate_auth_token()
    return jsonify({'token': token}), 201
