from flask import Blueprint

bp = Blueprint('tags', __name__, template_folder='templates')

from app.tags import routes