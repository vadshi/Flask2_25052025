from marshmallow import ValidationError, EXCLUDE
from api import db, app
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, change_author_schema

@app.post("/authors")
def create_author():
    try:
        # 1. Get raw bytes
        # print(f'{request.data =})
        # 2. Load bytes to dict
        # author_data = author_schema.loads(request.data)
        # print(f'{author_data = }, {type(author_data)})
        # 3. Create new AuthorModel instance via dict
        # author = AuthorModel(**author_data)
        author = author_schema.loads(request.data)  # get_data() return raw bytes
        db.session.add(author)
        db.session.commit()
    except ValidationError as ve:
        abort(400, f"Validation error: {str(ve)}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    # db instance -> dict -> json
    return jsonify(author_schema.dump(author)), 201


@app.get("/authors")
def get_authors():
    authors = db.session.scalars(db.select(AuthorModel)).all()
    return jsonify(author_schema.dump(authors, many=True)), 200


@app.get('/authors/<int:author_id>')
def get_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    # instance -> dict -> json
    return jsonify(author_schema.dump(author)), 200


@app.put("/authors/<int:author_id>")
def edit_authors(author_id: int):
    """ Update an existing quote """
    try:
        new_data = change_author_schema.load(request.json, unknown=EXCLUDE) # get_json() -> need load
    except ValidationError as ve:
        return abort(400, f"Validation error: {str(ve)}.")
    
    # Проверка на пустой словарь, т.е. есть данные для обновления
    if not new_data: # check that new_data is not {}
        return abort(400, "No valid data to update.")

    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")

    try:
        for key_as_attr, value in new_data.items():
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