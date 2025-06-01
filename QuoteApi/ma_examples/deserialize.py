from marshmallow import EXCLUDE, INCLUDE, RAISE, ValidationError
from author import Author
from schema import AuthorSchema

json_data = """
{  
   "id": 1,
   "name": "Ivan",
   "email": "ivan@mail.ru"
}
"""
try:
    schema = AuthorSchema()
    # json string -> validated dict
    json_data_as_dict = schema.loads(json_data, unknown=INCLUDE)
    print(type(json_data_as_dict), json_data_as_dict)
except ValidationError as e:
    print(e)

# dict > valildate dict
result = schema.load(json_data_as_dict, unknown=INCLUDE)
print(type(result), result)
print(Author(**result))