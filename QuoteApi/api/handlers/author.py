from marshmallow import ValidationError, EXCLUDE
from api import db, app, token_auth
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import AuthorSchema

@app.post("/authors")
@app.auth_required(token_auth)
@app.input(AuthorSchema, arg_name="author")
@app.output(AuthorSchema, status_code=201)
@app.doc(summary="Create new author", description="Create new author", responses=[503], tags=["Authors"])
def create_author(author):
    try:
        db.session.add(author)
        db.session.commit()
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    # db instance -> dict -> json
    return author


@app.get("/authors")
@app.output(AuthorSchema(many=True))
@app.doc(summary="Get all authors", description="Get all authors", tags=["Authors"])
def get_authors():
    return db.session.scalars(db.select(AuthorModel)).all(), 200


@app.get('/authors/<int:author_id>')
@app.output(AuthorSchema)
@app.doc(summary="Get author by id", description="Get author by id", tags=["Authors"])
def get_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    # instance -> dict -> json
    return author, 200


@app.put("/authors/<int:author_id>")
@app.auth_required(token_auth)
@app.input(AuthorSchema(load_instance=False, partial=True), arg_name="author_data")
@app.output(AuthorSchema)
@app.doc(summary="Get author by id", description="Get author by id", tags=["Authors"], responses=[400, 503])
def edit_authors(author_id: int, author_data):
    """ Update an existing author """
    
    # Проверка на пустой словарь, т.е. есть данные для обновления
    if not author_data: # check that new_data is not {}
        return abort(400, "No data to update.")

    author = db.get_or_404(entity=AuthorModel, ident=author_id, description=f"Author with id={author_id} not found")

    try:
        for key_as_attr, value in author_data.items():
            setattr(author, key_as_attr, value)

        db.session.commit()
        return author, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.delete("/authors/<int:author_id>")
@app.auth_required(token_auth)
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