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

from app.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix ='/admin')

from app.reports import bp as reports_db
app.register_blueprint(reports_db, url_prefix='/reports')

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

    # Create a sample (non-admin) user with email and password settings from environment variables
    person_username = os.environ.get('person_username')
    person_user = models.User (username = person_username)
    person_email = os.environ.get('person_email')
    person_user.email = person_email
    person_password = os.environ.get('person_password')
    person_user.set_password(person_password)
    person_user.is_administrator = False

    # Create a sample admin user as well
    admin_user = models.User (username='admin')
    admin_email = os.environ.get('admin_email')
    admin_user.email = admin_email
    admin_password = os.environ.get('admin_password')
    admin_user.set_password(admin_password)
    admin_user.is_administrator = True

    # Add in some data to the tags table
    research_tag = models.Tag(name = 'research')
    db.session.add(research_tag)
    career_tag = models.Tag(name = 'career')
    db.session.add(career_tag)
    teaching_tag = models.Tag(name = 'teaching')
    db.session.add(teaching_tag)
    admin_tag = models.Tag(name = 'administration')
    db.session.add(admin_tag)

    # Add tags to the sample non-admin user
    person_user.tags.append(research_tag)
    person_user.tags.append(career_tag)
    person_user.tags.append(teaching_tag)

    # Add tag to the sample admin user
    admin_user.tags.append(admin_tag)

    # Sample data for the dan user
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

    # Sample data for the admin user

    book3 = models.Book (
        title = 'Administration for Dummies',
        status = 'Started',
        priority = 'High',
    )
    book3.tags.append(admin_tag)
    db.session.add(book3)

    course2 = models.Course (
        title = 'Administration 101',
        status ='Not Started',
        priority = 'Medium'
    )
    course2.tags.append(admin_tag)
    db.session.add(book3)

    # Add the items (books and courses) to the example user
    person_user.items.append(book1)
    person_user.items.append(book2)
    person_user.items.append(course1)
    db.session.add(person_user)

    # Add the admin user and their items to the session
    admin_user.items.append(book3)
    admin_user.items.append(course2)
    db.session.add(admin_user)

    db.session.commit()

    print('Database was initalised successfully.')

