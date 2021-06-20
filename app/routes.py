from flask import render_template, request

from app import app, db
from app.models import Book

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.get('/books')
def books_list():
    books = Book.query.all()
    return render_template('books_list.html', title = 'Books', books = books)

@app.get('/books/<int:id>')
def view_book(id):
    book = Book.query.get_or_404(id)
    return render_template('book_details.html', title = book.title, book = book)

@app.route('/add_book', methods = ['GET','POST'])
def add_book():
    if request.method == 'GET':
        return render_template('add_book.html', title = 'Add book')
    else:
        book_title = request.form.get('book_title')
        status = request.form.get('status')
        priority = request.form.get('priority')

        # Create and add a book from the form
        # For now, we'll just use the mandatory fields
        # We'll use WTForms to create (and validate) these forms later
        new_book = Book (
            title = book_title,
            status = status,
            priority = priority
        )
        db.session.add(new_book)
        db.session.commit()

        return render_template(
            'book_success.html', 
            title = 'Added Book Successfully',
            book_title = book_title
        )