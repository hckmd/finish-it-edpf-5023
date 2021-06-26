from flask import render_template, request, url_for, redirect
from flask_login import login_required

from app import db
from app.models import User
from app.admin import bp
from .decorators import admin_required
from .forms import UserAddForm, UserEditDetailsForm

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


@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
        
    username = user.username
    page_title = f'Deleted {username}'
    db.session.delete(user)
    db.session.commit()
    return render_template('user_deleted.html', username = username, title = page_title)
