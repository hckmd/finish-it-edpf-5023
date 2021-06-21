from flask import render_template

from app import db
from app.models import Tag
from app.tags import bp

@bp.route('/')
@bp.route('/index')
def index():
    tags = Tag.query.all()
    return render_template('tags_list.html', title='Tags', tags=tags)