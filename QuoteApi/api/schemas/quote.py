from api import ma
from marshmallow import EXCLUDE, ValidationError, validates
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema
from marshmallow.validate import Length, Range


class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        dump_only = ("id",)
        unknown = EXCLUDE

    id = ma.auto_field()
    text = ma.auto_field(required=True, validate=Length(min=3))
    author_id = ma.auto_field()
    author = ma.Nested(AuthorSchema(only=("id", "name", "surname")))
    # rating = ma.auto_field(strict=True, validate=Range(1, 6))  # Variant 2
    rating = ma.Integer(strict=True)

    @validates('rating')
    def validate_rating(self, value, data_key: str):
        if value not in range(1, 6):
            raise ValidationError("Rating must be in in range(1, 6)")



quote_schema = QuoteSchema(exclude=["author_id"])
quotes_schema = QuoteSchema(many=True, exclude=["author"])
# use it when ValidationError.messages_dict contain only "rating" field error
change_quotes_without_rating = QuoteSchema(exclude=["rating"], partial=True)

