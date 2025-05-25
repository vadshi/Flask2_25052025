from flask import jsonify
from api import app
from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def handle_exception(e):
    """ Функция для перехвата HTTP ошибок и возврата в виде JSON."""
    return jsonify({"error": str(e)}), e.code