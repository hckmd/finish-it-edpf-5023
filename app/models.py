from app import db

book_tags = db.Table('book_tag',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('tag.id'))
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(100), nullable = False)
    priority = db.Column(db.String(100), nullable = False)
    next_steps = db.Column(db.Text)
    barriers = db.Column(db.Text)
    notes = db.Column(db.Text)
    tags = db.relationship(
        'Tag',
        secondary = book_tags,
        back_populates = 'books'
    )

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True, nullable = False)
    books = db.relationship(
        'Book',
        secondary = book_tags,
        back_populates = 'tags'
    )
    