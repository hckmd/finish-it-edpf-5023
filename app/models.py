from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(100), nullable = False)
    priority = db.Column(db.String(100), nullable = False)
    next_steps = db.Column(db.Text)
    barriers = db.Column(db.Text)
    notes = db.Column(db.Text)

    