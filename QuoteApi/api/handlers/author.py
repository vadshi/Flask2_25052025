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


@app.get("/authors")
def get_authors():
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    authors = [author.to_dict() for author in authors_db]
    return jsonify(authors), 200


@app.get('/authors/<int:author_id>')
def get_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    # instance -> dict -> json
    return jsonify(author.to_dict()), 200


