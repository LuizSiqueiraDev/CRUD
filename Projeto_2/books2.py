from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: int | None = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int
    
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'luiz',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2000
            }
        }


BOOKS = [
    Book(1, 'Conan', 'Robert E. Howard', 'Contos do barbaro hiboriano', 4, 1953),
    Book(2, 'Crônicas do matador de reis', 'Patrick Rothfuss', 'Tragédia e ascensão de um jovem', 5, 2007),
    Book(3, 'O chamado do Cthulhu', 'H. P. Lovecraft', 'conto sombrio e bizarro.', 2, 1928),
    Book(4, 'O Hobbit', 'J. R. R. Tolkien', 'Busca de um tesouro perdido', 3, 1937),
    Book(5, 'A torre negra', 'Stephen King', 'Um jovem que viaja atrás de um mago', 1, 1982),
    Book(6, 'Mistborn', 'Brandon Sanderson', 'Um grupo que luta contra a tirania', 3, 2006),
]


@app.get("/books")
async def mostrar_livros():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        

@app.get("/books/rating/{book_rating}")
async def read_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/date/{book_date}")
async def read_book_by_date(book_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break