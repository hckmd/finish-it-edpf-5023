from flask import render_template

from app import app
from app.models import Item

@app.route('/')
@app.route('/index')
def index():
    items = Item.query.all()
    return render_template('index.html', title = 'Home', items = items)

