from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, authors_schema

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
    authors = db.session.scalars(db.select(AuthorModel)).all()
    return jsonify(authors_schema.dump(authors)), 200


@app.get('/authors/<int:author_id>')
def get_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    # instance -> dict -> json
    return jsonify(author.to_dict()), 200


@app.put("/authors/<int:author_id>")
def edit_authors(author_id: int):
    """ Update an existing quote """
    new_data = request.json

    # Проверка на пустой словарь, т.е. есть данные для обновления
    if not new_data: # check that new_data is not {}
        return abort(400, "No valid data to update.")

    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")

    try:
        for key_as_attr, value in new_data.items():
            # Проверка на лишние ключи(атрибуты)
            if not hasattr(author, key_as_attr):
                abort(400, f"Invalid key='{key_as_attr}'. Valid only 'name' and 'surname'")
            setattr(author, key_as_attr, value)

        db.session.commit()
        return jsonify(author.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    """Delete author by id """
    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return jsonify({"message": f"Author with id {author_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")