from typing import List

from fastapi import HTTPException, status, APIRouter

from Exception.exception import AuthorNotFound, AuthorExisted, NoBooks, BookNotFound
from Models.schema import BookM, AuthorM
from Services.Crud import Crud

route = APIRouter()


@route.post("/add-book/", response_model=BookM)
async def add_book(book: BookM):
    try:
        return await Crud.add_book_service(book=book)
    except AuthorNotFound as not_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found.message)


@route.post("/add-author/", response_model=AuthorM)
async def add_author(author: AuthorM):
    try:
        return await Crud.add_author_service(author=author)
    except AuthorExisted as exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exist.message)


@route.get("/books/", response_model=List[BookM])
async def get_books():
    try:
        return await Crud.get_books_service()
    except NoBooks as empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=empty.message)


@route.get("/books/{book_id}", response_model=BookM)
async def get_book(book_id: int):
    try:
        book = await Crud.get_book_service(book_id=book_id)
        return book
    except BookNotFound as not_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found.message)


@route.delete("/books/{Book_id}", response_model=BookM)
async def delete_book(book_id: int):
    try:
        book = await Crud.get_book_service(book_id=book_id)
        await Crud.delete_book_service(book)
        return "successfully deleted the book"
    except BookNotFound as not_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found.message)


@route.put("/books/{book_id}", response_model=BookM)
async def update_book(book_id: int, book_data: BookM):
    try:
        book = await Crud.get_book_service(book_id=book_id)
        return await Crud.update_book_service(book_data=book_data, book=book)
    except BookNotFound as not_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found.message)
