from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user

from app import db
from app.courses import bp
from app.models import Course, Tag
from .forms import CourseEditForm, CourseAddForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    courses = Course.query.filter_by(user_id = current_user.id)
    return render_template (
        'courses_list.html',
        title='Courses',
        courses=courses
    )

@bp.route('/<int:id>/edit', methods = ['GET','POST'])
@login_required
def edit(id):
    course = Course.query.get_or_404(id)
    # Double check that the user trying to edit this course actually
    # owns the course that is being edited (if not, this is unauthorised)
    if course.user_id != current_user.id:
        return render_template('unauthorized.html'), 401
    form = CourseEditForm(obj=course)
    page_title = f'Editing {course.title}'
    if form.validate_on_submit():
        form.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('courses.view', id = course.id))

    return render_template(
        'edit_course.html', 
        title = page_title, 
        course_id = id,
        form = form
    )

@bp.get('/<int:id>')
@login_required
def view(id):
    course = Course.query.get_or_404(id)
    # Double check that the user accessing this course actually owns it
    if course.user_id != current_user.id:
        return render_template('unauthorized.html'), 401
    return render_template('course_details.html', title = course.title, course = course)

@bp.route('/add_course', methods = ['GET','POST'])
@login_required
def add():
    form = CourseAddForm()
    if form.validate_on_submit():
        course = Course()

        # We'll map the fields across from the form to the database object
        # Instead of using populate_obj, because there are some steps involved 
        # in adding the course's tags
        course.title = form.title.data
        course.url = form.url.data
        course.status = form.status.data
        course.priority = form.priority.data
        course.next_steps = form.next_steps.data
        course.barriers = form.barriers.data
        course.notes = form.notes.data

        # Set the user of the course to the logged in user
        course.user_id = current_user.id

        # Add the tags we need
        selected_tag_ids = form.tags.data
        for selected_tag_id in selected_tag_ids:
            tag = Tag.query.get(selected_tag_id)
            course.tags.append(tag)

        db.session.add(course)
        db.session.commit()
        
        return render_template(
            'course_success.html', 
            title = 'Added Course Successfully',
            course_title = course.title
        )
        
    return render_template('add_course.html', title = 'Add course', form = form)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    course = Course.query.get_or_404(id)

    # Double check that the user is trying to delete actually
    # owns the course (if not, this is unauthorised)
    if course.user_id != current_user.id:
        return render_template('unauthorized.html'), 401

    course_title = course.title
    page_title = f'Deleted {course_title}'
    db.session.delete(course)
    db.session.commit()
    return render_template('course_deleted.html', course_title = course_title, title = page_title)

@bp.route('/<int:id>/tags', methods = ['GET', 'POST'])
@login_required
def edit_tags(id):
    course = Course.query.get_or_404(id)

    # Double check that the user trying to edit tags
    # owns the course that is being edited (if not, this is unauthorised)
    if course.user_id != current_user.id:
        return render_template('unauthorized.html'), 401

    course_tag_ids = [tag.id for tag in course.tags]
    tags = Tag.query.filter_by(user_id = current_user.id)

    if request.method == 'POST':
        selected_tag_ids = request.form.getlist('tag-checkboxes')
        selected_tag_ids = [int(id) for id in selected_tag_ids]
        course.update_tags(selected_tag_ids)
        return redirect(url_for('courses.view', id = course.id))

    return render_template('course_tags.html', 
        course = course,
        tags = tags,
        course_tag_ids = course_tag_ids, 
        title = 'Edit Course tags',
    )