from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.models import Tag
from app.tags import bp
from .forms import TagAddForm, TagEditForm

@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    editing = False
    edit_tag = None
    editing_tag_id = 0
    add_form = TagAddForm()
    edit_form = TagEditForm()

    if 'tag_id' in request.args:
        editing_tag_id = int(request.args['tag_id'])
        edit_tag = Tag.query.get_or_404(editing_tag_id)
        # Check that the tag the user is editing is actually theirs
        if edit_tag.user_id == current_user.id:
            editing = True
            edit_form = TagEditForm(obj=edit_tag)
        else:
            # The user is trying to edit someone else's tag,
            # which is an unauthorised requesst
            return render_template('unauthorized.html'), 401
    tags = Tag.query.filter_by(user_id=current_user.id)

    if add_form.validate_on_submit():
        print('Running this add_form')
        tag = Tag()
        add_form.populate_obj(tag)
        tag.user_id = current_user.id
        db.session.add(tag)
        db.session.commit()

        return redirect(url_for('tags.index'))

    return render_template('tags_list.html', 
        title='Tags', tags=tags, 
        editing = editing, editing_tag_id=editing_tag_id,
        add_form=add_form, edit_form=edit_form
    )

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    to_delete = Tag.query.get_or_404(id)
    # Check that the tag the user is deleting is actually theirs
    if to_delete.user_id == current_user.id:
        tag_name = to_delete.name
        db.session.delete(to_delete)
        db.session.commit()
    else:
        # The user is trying to delete someone else's tag,
        # which is an unauthorised requesst
        return render_template('unauthorized.html'), 401
        
    return render_template('tag_delete_success.html', title='Tag Deleted', tag_name=tag_name)

@bp.post('/save/<int:id>')
@login_required
def save(id):
    edit_form = TagEditForm()
    add_form = TagAddForm()
    tags = Tag.query.filter_by(user_id=current_user.id)
    if edit_form.validate_on_submit():
        tag = Tag.query.get_or_404(id)
        # Check that the tag the user is saving is actually theirs
        if tag.user_id == current_user.id:
            edit_form.populate_obj(tag)
            db.session.add(tag)
            db.session.commit()
        else:
            # The user is trying to edit someone else's tag,
            # which is an unauthorised requesst
            return render_template('unauthorized.html'), 401
        
        return redirect(url_for('tags.index'))

    return render_template('tags_list.html', 
        title='Tags', tags=tags, 
        editing = True, editing_tag_id=id,
        add_form=add_form, edit_form=edit_form
    )