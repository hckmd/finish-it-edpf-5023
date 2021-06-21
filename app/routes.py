from os import stat
from flask import render_template, request, redirect, url_for

from app import app
from app import status_options, priority_options
from app.models import Book, Tag

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')


