from flask import Blueprint

bp = Blueprint('courses', __name__, template_folder='templates')

from app.courses import routes