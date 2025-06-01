from api import ma
from marshmallow import EXCLUDE
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema
from marshmallow.validate import Length

def rating_validate(value: int):
    """ Example of custom validator """
    # if return True -> validation success
    # if return False -> raise ValidationError
    return value in range(1, 6)


class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        dump_only = ("id",)
        unknown = EXCLUDE

    id = ma.auto_field()
    text = ma.auto_field(required=True, validate=Length(min=3))
    author_id = ma.auto_field()
    author = ma.Nested(AuthorSchema(only=("id", "name", "surname")))
    rating = ma.auto_field(strict=True, validate=rating_validate)


quote_schema = QuoteSchema(exclude=["author_id"])
quotes_schema = QuoteSchema(many=True, exclude=["author"])
# use it when ValidationError.messages_dict contain only "rating" field error
change_quotes_without_rating = QuoteSchema(exclude=["rating"], partial=True)

