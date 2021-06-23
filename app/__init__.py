import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the app and set up different configuration settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this-is-a-secret' # Not for use in production, just a demo

# Create the db and hard-coded values shared in different blueprints
db = SQLAlchemy(app)
STATUS_OPTIONS = ['Not Started', 'Started', 'Completed', 'On Hold']
PRIORITY_OPTIONS = ['Low', 'Medium', 'High']

# Set up flask-login for user authentication
login = LoginManager(app)

# Register the different blueprints (modules) in the app
from app.books import bp as books_bp
app.register_blueprint(books_bp, url_prefix='/books')

from app.tags import bp as tags_bp
app.register_blueprint(tags_bp, url_prefix='/tags')

from app.courses import bp as courses_bp
app.register_blueprint(courses_bp, url_prefix='/courses')

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix ='/auth')

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

    # Create a sample user with email and password settings from .env
    dan_user = models.User (username='dan')
    env_email = os.environ.get('dan_email')
    dan_user.email = env_email
    env_password = os.environ.get('dan_password')
    dan_user.set_password(env_password)

    # Add in some data to the tags table
    research_tag = models.Tag(name = 'research')
    db.session.add(research_tag)
    career_tag = models.Tag(name = 'career')
    db.session.add(career_tag)
    teaching_tag = models.Tag(name = 'teaching')
    db.session.add(teaching_tag)

    # Add in some data to the books table
    book1 = models.Book (
        title = 'Beyond Doctorates Downunder',
        status = 'Started',
        priority = 'Medium'
    )               
    book1.tags.append(research_tag)
    book1.tags.append(career_tag)
    db.session.add(book1)

    book2 = models.Book (
        title = 'Train the Trainer',
        status = 'Started',
        priority = 'High'
    )
    book2.tags.append(teaching_tag)
    db.session.add(book2)

    course1 = models.Course (
        title = 'Certified Peer Reviewer Course',
        status = 'Started',
        priority = 'Medium',
        url = 'https://researcheracademy.elsevier.com/navigating-peer-review/certified-peer-reviewer-course'
    )
    course1.tags.append(research_tag)
    course1.tags.append(career_tag)
    db.session.add(course1)

    # Add the items (books and courses) to the example user
    dan_user.items.append(book1)
    dan_user.items.append(book2)
    dan_user.items.append(course1)
    db.session.add(dan_user)

    db.session.commit()

