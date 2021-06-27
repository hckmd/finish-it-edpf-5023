from flask.templating import render_template
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, flash

from app.models import User
from app.auth import bp
from .forms import LoginForm

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form = form)

@bp.route('logout')
def logout():
    logout_user()
    return redirect(url_for('index'))