from flask import render_template
from flask_login import login_required

from app.models import User
from app.admin import bp
from .decorators import admin_required

@bp.get('/')
@bp.get('/index')
@login_required
@admin_required
def index():
    users = User.query.all()
    print(users)
    return render_template('user_list.html', title = 'Users', users = users)