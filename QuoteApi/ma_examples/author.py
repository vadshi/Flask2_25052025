class Author:
    def __init__(self, id, name, email="my_mail@mail.ru"):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Author({self.id}, {self.name}, {self.email})"
