from flask import render_template, request, url_for, flash, redirect
from flask_login import current_user, login_required

from app import app
from app.models import Item, Tag

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

