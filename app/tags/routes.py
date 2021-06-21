from flask import render_template, redirect, url_for

from app import db
from app.models import Tag
from app.tags import bp
from .forms import TagAddForm

@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
def index():
    tags = Tag.query.all()
    form = TagAddForm()
    if form.validate_on_submit():
        tag = Tag()
        form.populate_obj(tag)
        db.session.add(tag)
        db.session.commit()

        return redirect(url_for('tags.index'))

    return render_template('tags_list.html', title='Tags', tags=tags, form=form)

@bp.route('/delete/<int:id>')
def delete(id):
    to_delete = Tag.query.get_or_404(id)
    tag_name = to_delete.name
    db.session.delete(to_delete)
    db.session.commit()
    return render_template('tag_delete_success.html', title='Tag Deleted', tag_name=tag_name)
