from fastapi import Body, FastAPI

app = FastAPI()
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'Math'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'History'},

]
@app.get("/books")
def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
def read_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
def read_by_category(category: str):
    books_to_return=[]
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
           books_to_return.append(book)
    return books_to_return
    
@app.get("/books/{book_category}/")
def read_author_category(author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and book.get('category') == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_new_data")
def add_data(new_data=Body()):
    BOOKS.append(new_data)
    
@app.put("/books/update_book")
def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == updated_book.get('author').casefold():
            BOOKS[i] = updated_book
            
@app.delete("/books/delete_book/{book_title}")
def Delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
    
    
    
    
