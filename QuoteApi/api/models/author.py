from api import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from api.models.quote import QuoteModel


class AuthorModel(db.Model):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    # default -> for new instance, server_default -> for instances that already exist in table
    surname: Mapped[str] = mapped_column(String(32), default="Petrov", server_default="Smirnov", index=True)
    quotes: Mapped[list['QuoteModel']] = relationship(lambda: QuoteModel, back_populates='author', lazy='dynamic', cascade="all, delete-orphan") # type: ignore

    def __init__(self, name, surname="Petrov"):
        self.name = name
        self.surname = surname
    
    def __str__(self):
        repr(self)

    def __repr__(self):
        return f'Author{self.name, self.surname}'    