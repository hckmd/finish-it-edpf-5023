import json

from flask import render_template, request, url_for, flash, redirect, Response
from flask_login import current_user, login_required

from app import app
from app.models import Item, Tag
from app.utils import export_user_items, import_user_items

@app.errorhandler(401)
def unauthorised(e):
    if current_user.is_authenticated:
        flash('You do not have access to this part of the app.')
        render_template('unauthorized.html')
    else:
        flash('Please login to access the app.')
        return(redirect(url_for('auth.login')))

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        items = Item.query.filter_by(user_id = current_user.id)
        return render_template('index.html', title = 'Home', items = items)
    else:
        return redirect(url_for('auth.login'))

@app.route('/view_by_tag')
@login_required
def view_by_tag():
    all_tags = Tag.query.filter_by(user_id = current_user.id)
    selected_tags = None
    selected_tag_id = 0
    # Check if the tag id is a placeholder, when no tag has been selected
    if 'tag_id' in request.args and request.args['tag_id'] != '-':
        tag_id = request.args['tag_id']
        selected_tag_id = int(tag_id)
        selected_tags = Tag.query.filter_by(id = selected_tag_id, user_id = current_user.id)
    else:
        selected_tags = all_tags
    return render_template('by_tag.html', 
        title = 'View by tag', all_tags = all_tags, selected_tags = selected_tags, selected_tag_id = selected_tag_id
    )

@app.get('/export_items')
@login_required
def export_items():
    items = Item.query.filter_by(user_id = current_user.id)
    export = export_user_items(items)
    return Response(json.dumps(export), mimetype='application/json', 
        headers={'Content-Disposition':'attachment;filename=items.json'})

def allowed_file(filename):
    # Code adapted from https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == "json"

@app.post('/import_items')
@login_required
def import_items():

    # Check that the user has chosen a file to upload
    if 'file' not in request.files:
        flash('No file was chosen to export.', 'error')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file.', 'error')
        return redirect(url_for('index'))

    # Check that the file is of a type that can be imported
    if file and not allowed_file(file.filename):
        flash('Uploaded file should be a .json file', 'error')
        return redirect(url_for('index'))
    
    # Process the file to import the items for the current user
    import_result = import_user_items(file, current_user.id)
    if import_result.success:
        imported_message = f'{import_result.imported} items were imported.'
        flash(imported_message, 'info')
    else:
        for message in import_result.messages:
            flash(message, 'error')

    return redirect(url_for('index'))

