from flask import render_template, request

from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.get('/books')
def books_list():
    return render_template('books_list.html', title = 'Books')

@app.route('/add_book', methods = ['GET','POST'])
def add_book():
    if request.method == 'GET':
        return render_template('add_book.html', title = 'Add book')
    else:
        return render_template('book_success.html', title = 'Added Book Successfully')