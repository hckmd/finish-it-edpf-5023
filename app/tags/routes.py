from flask import render_template, redirect, url_for, request

from app import db
from app.models import Tag
from app.tags import bp
from .forms import TagAddForm, TagEditForm

@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
def index():
    editing = False
    edit_tag = None
    editing_tag_id = 0
    add_form = TagAddForm()
    edit_form = TagEditForm()

    if 'tag_id' in request.args:
        editing_tag_id = int(request.args['tag_id'])
        edit_tag = Tag.query.get_or_404(editing_tag_id)
        editing = True
        edit_form = TagEditForm(obj=edit_tag)
    tags = Tag.query.all()

    if add_form.validate_on_submit():
        print('Running this add_form')
        tag = Tag()
        add_form.populate_obj(tag)
        db.session.add(tag)
        db.session.commit()

        return redirect(url_for('tags.index'))

    return render_template('tags_list.html', 
        title='Tags', tags=tags, 
        editing = editing, editing_tag_id=editing_tag_id,
        add_form=add_form, edit_form=edit_form
    )

@bp.route('/delete/<int:id>')
def delete(id):
    to_delete = Tag.query.get_or_404(id)
    tag_name = to_delete.name
    db.session.delete(to_delete)
    db.session.commit()
    return render_template('tag_delete_success.html', title='Tag Deleted', tag_name=tag_name)

@bp.post('/save/<int:id>')
def save(id):
    edit_form = TagEditForm()
    add_form = TagAddForm()
    tags = Tag.query.all()
    if edit_form.validate_on_submit():
        tag = Tag.query.get_or_404(id)
        edit_form.populate_obj(tag)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('tags.index'))

    return render_template('tags_list.html', 
        title='Tags', tags=tags, 
        editing = True, editing_tag_id=id,
        add_form=add_form, edit_form=edit_form
    )