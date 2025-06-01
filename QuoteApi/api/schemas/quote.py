from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema


def rating_validate(value: int):
    """ Example of custom validator """
    # if return True -> validation success
    # if return False -> raise ValidationError
    return value in range(1, 6)


class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        # load_instance = True

    id = ma.auto_field()
    text = ma.auto_field()
    author = ma.Nested(AuthorSchema(only=("name")))
    rating = ma.Integer(strict=True, validate=rating_validate)


quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)

