from marshmallow import ValidationError
from api import db, app
from flask import abort, jsonify, request
from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from api.schemas.quote import quote_schema, quotes_schema, change_quotes_without_rating


@app.get("/quotes")
def get_quotes():
    """ Функция возвращает все цитаты из БД. """
    quotes = db.session.scalars(db.select(QuoteModel)).all()
    return jsonify(quotes_schema.dump(quotes)), 200


# URL: "/authors/<int:author_id>/quotes"
@app.route("/authors/<int:author_id>/quotes", methods=["GET", "POST"])
def author_quotes(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    if request.method == "GET":
        return jsonify({"author": author.name, "quotes": quotes_schema.dump(list(author.quotes))}), 200

    elif request.method == "POST":
        try:
            data = quote_schema.loads(request.data)
            new_quote = QuoteModel(author, **data)
            db.session.add(new_quote)
            db.session.commit()
        except ValidationError as ve:
            abort(400, f"{ve.messages_dict}")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(503, f"Database error: {str(e)}")
       
        return jsonify(quote_schema.dump(new_quote)), 201
    else:
        abort(405)


@app.get("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id: int):
    """ Return quote by id from db."""
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")
    return jsonify(quote_schema.dump(quote)), 200



@app.get("/quotes/count")
def get_quotes_count() -> int:
    """ Return count of quotes in db."""
    count = db.session.scalar(func.count(QuoteModel.id))
    return jsonify(count=count), 200


@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id: int):
    """TODO. Update edit using ma """
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")

    try:
        data = quote_schema.loads(request.data)
    except ValidationError as ve:
        if "rating" in ve.messages_dict:
            data = change_quotes_without_rating.loads(request.data)

    for key_as_attr, value in data.items():
        setattr(quote, key_as_attr, value)

    try:
        db.session.commit()   
        return quote_schema.dump(quote), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


       

@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    """Delete quote by id """
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")
    db.session.delete(quote)
    try:
        db.session.commit()
        return jsonify({"message": f"Quote with id {quote_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
    
    
@app.route("/quotes/filter", methods=['GET'])
def filter_quotes():
    data = request.args # get query parameters from URL
    try:
        quotes = db.session.scalars(db.select(QuoteModel).filter_by(**data)).all()
    except InvalidRequestError:
        abort(400, f"Invalid data. Required: <author> and <text>. Received: {', '.join(data.keys())}")
    
    return jsonify(quotes_schema.dump(quotes)), 200