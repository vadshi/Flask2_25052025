from author import Author
from schema import AuthorSchema


author = Author("1", "Alex", "alex5@mail.ru")

author_schema = AuthorSchema()
# instance(экземпляр) -> dict
result = author_schema.dump(author)
print(type(result), result)
