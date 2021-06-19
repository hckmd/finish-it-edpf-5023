import os

import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes, models

# Command line functions for setting up a database

@app.cli.command('recreate-db')
def recreate_database():
    # Delete all tables and create them again
    db.drop_all()
    db.create_all()

@app.cli.command('init-db')
def init_database():

    # Start from scratch
    db.drop_all()
    db.create_all()

    # Add in some data to the books table
    book1 = models.Book (
        title = 'Beyond Doctorates Downunder',
        status = 'Started',
        priority = 'Medium'
    )               
    db.session.add(book1)

    book2 = models.Book (
        title = 'Train the Trainer',
        status = 'Started',
        priority = 'High'
    )
    db.session.add(book2)

    db.session.commit()

