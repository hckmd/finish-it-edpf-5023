from flask import render_template

from app import db
from app.courses import bp
from app.models import Course

@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
def index():
    courses = Course.query.all()
    print(courses)
    return render_template (
        'courses_list.html',
        title='Courses',
        courses=courses
    )

@bp.route('/<int:id>')
def view(id):
    return 'Not implemented yet'

@bp.route('/add_book')
def add():
    return 'Not implemented yet'