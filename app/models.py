from werkzeug.security import generate_password_hash, check_password_hash

from app import db

item_tags = db.Table('item_tag',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Item', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(100), nullable = False)
    priority = db.Column(db.String(100), nullable = False)
    next_steps = db.Column(db.Text)
    barriers = db.Column(db.Text)
    notes = db.Column(db.Text)
    type = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship(
        'Tag',
        secondary = item_tags,
        back_populates = 'items'
    )
    

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'item'
    }

    def update_tags(self, selected_tag_ids):

        # Get all the tags in the system
        all_tags = Tag.query.all()
        current_tag_ids = [tag.id for tag in self.tags]
        
        # Variable to keep track of changes made, to know whether to write to the db
        made_changes = False
        for tag in all_tags:
       
            # Check if any new tags need to be added to the item
            if tag.id in selected_tag_ids and tag.id not in current_tag_ids:
                self.tags.append(tag)
                db.session.add(self)
                made_changes = True

            # Check if any tags have been unselected and remove them from the item
            if tag.id in current_tag_ids and tag.id not in selected_tag_ids:
                self.tags.remove(tag)
                db.session.add(self)
                made_changes = True
        
        print(made_changes)
        # Changes have been made to the data, so we need to commit these
        if made_changes:
            db.session.commit()

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
    