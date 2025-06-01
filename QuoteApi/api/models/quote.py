from api import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class QuoteModel(db.Model):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[str] = mapped_column(ForeignKey('authors.id'))
    author: Mapped['AuthorModel'] = relationship(back_populates='quotes') # type: ignore
    text: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int] = mapped_column(server_default="1")

    def __init__(self, author, text, rating=1):
        self.author = author
        self.text  = text
        self.rating = rating

    def __repr__(self):
        return f'Quote{self.id, self.author}'  
    
    def to_dict(self):
        return {
            "quote_id": self.id,
            "text": self.text,
            "rating": self.rating
        }