from flask import render_template

from app import db
from app.models import Tag
from app.tags import bp

@bp.route('/')
@bp.route('/index')
def index():
    tags = Tag.query.all()
    return render_template('tags_list.html', title='Tags', tags=tags)

@bp.route('/delete/<int:id>')
def delete(id):
    to_delete = Tag.query.get_or_404(id)
    tag_name = to_delete.name
    db.session.delete(to_delete)
    db.session.commit()
    return render_template('tag_delete_success.html', title='Tag Deleted', tag_name=tag_name)