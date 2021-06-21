from app import db

item_tags = db.Table('item_tag',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(100), nullable = False)
    priority = db.Column(db.String(100), nullable = False)
    next_steps = db.Column(db.Text)
    barriers = db.Column(db.Text)
    notes = db.Column(db.Text)
    tags = db.relationship(
        'Tag',
        secondary = item_tags,
        back_populates = 'items'
    )
    type = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'item'
    }

class Book(Item):
    authors = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity':'book'
    }

class Course(Item):
    url = db.Column(db.String(200))

    __mapper_args__ = {
        'polymorphic_identity':'course'
    }

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True, nullable = False)
    items = db.relationship(
        'Item',
        secondary = item_tags,
        back_populates = 'tags'
    )
    