from flask import render_template, redirect, url_for, request

from app import db
from app.models import Book, Tag
from app.books import bp
from .forms import BookEditForm, BookAddForm

@bp.get('/')
def index():
    books = Book.query.all()
    return render_template('books_list.html', title = 'Books', books = books)

@bp.get('/<int:id>')
def view(id):
    book = Book.query.get_or_404(id)
    return render_template('book_details.html', title = book.title, book = book)

@bp.route('/<id>/edit', methods = ['POST', 'GET'])
def edit(id):
    book = Book.query.get_or_404(id)
    form = BookEditForm(obj=book)
    page_title = f'Editing {book.title}'
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.view', id = book.id))

    return render_template(
        'edit_book.html', 
        title = page_title, 
        book_id = id,
        form = form
    )

@bp.get('/delete/<int:id>')
def delete(id):
    book = Book.query.get_or_404(id)
    book_title = book.title
    page_title = f'Deleted {book_title}'
    db.session.delete(book)
    db.session.commit()
    return render_template('book_deleted.html', book_title = book_title, title = page_title)

@bp.route('/add_book', methods = ['GET','POST'])
def add():
    form = BookAddForm()
    if form.validate_on_submit():
        book = Book()
        print(form.tags.data)

        # We'll map the fields across from the form to the database object
        # Instead of using populate_obj, because there are some steps involved 
        # in adding the book's tags
        book.title = form.title.data
        book.authors = form.authors.data
        book.status = form.status.data
        book.priority = form.priority.data
        book.next_steps = form.next_steps.data
        book.barriers = form.barriers.data
        book.notes = form.notes.data

        # Add the tags we need
        selected_tag_ids = form.tags.data
        for selected_tag_id in selected_tag_ids:
            tag = Tag.query.get(selected_tag_id)
            book.tags.append(tag)

        db.session.add(book)
        db.session.commit()
        
        return render_template(
            'book_success.html', 
            title = 'Added Book Successfully',
            book_title = book.title
        )
        
    return render_template('add_book.html', title = 'Add book', form = form)
    
@bp.route('/<int:id>/tags', methods = ['GET', 'POST'])
def edit_tags(id):
    book = Book.query.get_or_404(id)
    book_tag_ids = [tag.id for tag in book.tags]
    tags = Tag.query.all()
    print(book_tag_ids)
    if request.method == 'POST':
        selected_tag_ids = request.form.getlist('tag-checkboxes')
        selected_tag_ids = [int(id) for id in selected_tag_ids]
        print(selected_tag_ids)

        # Variable to keep track of changes made, to know whether to write to the db
        made_changes = False
        for tag in tags:

            # Check if any new tags need to be added to the book
            if tag.id in selected_tag_ids and tag.id not in book_tag_ids:
                book.tags.append(tag)
                db.session.add(book)
                made_changes = True

            # Check if any tags have been unselected and remove them from the book
            if tag.id in book_tag_ids and tag.id not in selected_tag_ids:
                book.tags.remove(tag)
                db.session.add(book)
                made_changes = True
        
        # Changes have been made to the data, so we need to commit these
        if made_changes:
            db.session.commit()

        return redirect(url_for('books.view', id = book.id))

    return render_template('book_tags.html', 
        book = book,
        tags = tags,
        book_tag_ids = book_tag_ids, 
        title = 'Edit Book tags',
    )