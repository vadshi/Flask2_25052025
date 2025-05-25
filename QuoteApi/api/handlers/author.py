from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel


@app.post("/authors")
def create_author():
    author_data = request.json
    try:
        author = AuthorModel(**author_data)
        db.session.add(author)
        db.session.commit()
    except TypeError:
        abort(400, f"Invalid data. Required: <name>. Received: {', '.join(author_data.keys())}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify(author.to_dict()), 201


