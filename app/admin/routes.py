from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required

from app import db
from app.models import User
from app.admin import bp
from .decorators import admin_required
from .forms import UserAddForm, UserEditDetailsForm, UserChangePasswordForm

@bp.get('/')
@bp.get('/index')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('user_list.html', title = 'Users', users = users)

@bp.route('/add_user', methods = ['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserAddForm()
    if form.validate_on_submit():
        user = User()
        
        # Populate the new user from the form
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.is_administrator = form.is_administrator.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.index'))

    return render_template('add_user.html', title = 'Add User', form = form)


@bp.route('/edit_user/<int:id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserEditDetailsForm(obj=user)
    page_title = f'Editing {user.username} details'
    if form.validate_on_submit():

        # This view only allows change of name and email address
        # Changing password is a separate view
        user.username = form.username.data
        user.email = form.email.data
        user.is_administrator = form.is_administrator.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.index'))

    return render_template(
        'edit_user.html', 
        title = page_title, 
        form = form
    )

def format_delete_message(username, type, multiple):
    '''Helper function for formatting messages on deletion'''
    message = ''
    if multiple:
        message = f'{username} has {type}s in the system. Please delete these before deleting the user.'
    else:
        message = f'{username} has a {type} in the system. Please delete this before deleting the user.'
    return message

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    username = user.username
    to_delete = True
    
    # Check if the user has items or tags
    # Prevent deletion if they have any of these
    # User will have to delete all of these before deleting the user
    if len(user.items) > 0:
        to_delete = False

        # Check if the user has books in the system
        books = [item for item in user.items if item.type == 'book']
        if len(books) > 0:
            message = format_delete_message(username, 'book', len(books) == 1)
            flash(message, 'error')

        # Check if the user has courses in the system
        courses = [item for item in user.items if item.type == 'course']
        if len(courses) > 0:
            message = format_delete_message(username, 'course', len(courses) == 1)
            flash(message, 'error')

    if len(user.tags) > 0:
        to_delete = False
        message = format_delete_message(username, 'tag', len(user.tags) == 1)
        flash(message, 'error')

    page_title = f'Deleting {username}'
    if to_delete:
        page_title = f'Deleted {username}'
        db.session.delete(user)
        db.session.commit()
        return render_template('user_deleted.html', username = username, title = page_title)

    return redirect(url_for('admin.index'))

@bp.route('/change_password/<int:user_id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def change_password(user_id):
    user = User.query.get_or_404(user_id)
    form = UserChangePasswordForm(obj=user)
    page_title = f'Changing password for {user.username}'
    if form.validate_on_submit():

        # This view just changes password of a user
        # Changing user details is in a separate view
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.index'))

    return render_template(
        'change_password.html', 
        title = page_title, 
        form = form
    )
