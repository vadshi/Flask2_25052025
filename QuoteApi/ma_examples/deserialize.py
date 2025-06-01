from marshmallow import EXCLUDE, INCLUDE, RAISE, ValidationError
from author import Author
from schema import AuthorSchema
from pprint import pprint


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
    json_data_as_dict = schema.loads(json_data)
    print(type(json_data_as_dict), json_data_as_dict)
except ValidationError as e:
    print(e)

# dict > valildate dict
result = schema.load(json_data_as_dict)
print(type(result), result)
print(Author(**result))

json_data_list = """
[
   {
       "id": 1,
       "name": "Alex",
       "email": "alex@mail.ru"
   },
   {
       "id": 2,
       "name": "Ivan",
       "email": "ivan@mail.ru"
   },
   {
       "id": 4,
       "name": "Tom",
       "email": "tom@mail.ru"
   }
]
"""
# При обработке списка, необходимо указать параметр many=True
# либо при создании экземпляра схемы либо при вызове методов load/loads
# Variant 1
authors_schema = AuthorSchema(many=True)
result_one = authors_schema.loads(json_data_list)

pprint(result_one, sort_dicts=False)

# Variant 2
result_two = schema.loads(json_data_list, many=True)
print('\n=== Repeat ===\n')
pprint(result_two, sort_dicts=False)