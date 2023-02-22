from typing import List

from Database.database import session_local
from Exception.exception import AuthorExisted, AuthorNotFound, NoBooks, BookNotFound
from Models.models import Book, Author
from Models.schema import BookM, AuthorM


class Crud:
    def __init__(self):
        self.db = session_local

    @staticmethod
    async def add_book_service(self, book: BookM) -> BookM:
        try:
            db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
            self.db.add(db_book)
            self.db.commit()
            self.db.refresh(db_book)
        except Exception as error:
            raise AuthorNotFound
        return BookM.from_orm(db_book)

    @staticmethod
    async def add_author_service(self, author: AuthorM) -> AuthorM:
        try:
            db_author = Author(name=author.name, age=author.age)
            self.db.add(db_author)
            self.db.commit()
            self.db.refresh(db_author)
        except Exception as error:
            raise AuthorExisted

        return db_author

    @staticmethod
    async def get_books_service(self) -> List[BookM]:
        try:
            books = self.db.query(Book).all()
            return list(map(BookM.from_orm, books))
        except Exception as error:
            raise NoBooks

    @staticmethod
    async def get_book_service(self, book_id: int):
        try:
            book = self.db.query(Book).filter(Book.id == book_id).first()
            return book
        except Exception as error:
            raise BookNotFound

    @staticmethod
    async def delete_book_service(self, book: Book):
        try:
            self.db.delete(book)
            self.db.commit()
        except Exception as error:
            raise BookNotFound

    @staticmethod
    async def update_book_service(self, book_data: BookM, book: Book) -> BookM:
        try:
            book.title = book_data.title
            book.rating = book_data.rating
            book.author_id = book_data.author_id

            self.db.commit()
            self.db.refresh(book)

            return BookM.from_orm(book)
        except Exception as error:
            raise BookNotFound
