from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect

from app import db
from app.courses import bp
from app.models import Course
from .forms import CourseEditForm

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

@bp.route('/edit/<int:id>', methods = ['GET','POST'])
def edit(id):
    course = Course.query.get_or_404(id)
    form = CourseEditForm(obj=course)
    page_title = f'Editing {course.title}'
    if form.validate_on_submit():
        form.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('courses.index'))

    return render_template(
        'edit_course.html', 
        title = page_title, 
        book_id = id,
        form = form
    )

@bp.route('/<int:id>')
def view(id):
    # Temporarily redirect to edit page for the course, to be replaced later
    return redirect(url_for('courses.edit', id=id))

@bp.route('/add_course')
def add():
    return 'Not implemented yet'