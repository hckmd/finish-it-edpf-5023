from flask import render_template, request

from app import app
from app.models import Item, Tag

@app.route('/')
@app.route('/index')
def index():
    items = Item.query.all()
    return render_template('index.html', title = 'Home', items = items)

@app.route('/view_by_tag')
def view_by_tag():
    all_tags = Tag.query.all()
    selected_tags = None
    selected_tag_id = 0
    # Check if the tag id is a placeholder, when no tag has been selected
    if 'tag_id' in request.args and request.args['tag_id'] != '-':
        tag_id = request.args['tag_id']
        selected_tag_id = int(tag_id)
        selected_tags = Tag.query.filter_by(id=selected_tag_id)
    else:
        selected_tags = all_tags
    return render_template('by_tag.html', 
        title = 'View by tag', all_tags = all_tags, selected_tags = selected_tags, selected_tag_id = selected_tag_id
    )

