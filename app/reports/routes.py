import json

from flask import render_template
from flask_login import login_required, current_user
import plotly
import plotly.express as px
from sqlalchemy import func

from app import db
from app.reports import bp
from app.models import Item

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('reports.html', title = 'Reports')

@bp.route('/item_status')
@login_required
def item_status():
    # Queries the Items table to get the number of items for status and type
    item_status_data = db.session.query(
        Item.status, Item.type, func.count(Item.id).label('count')
        ).filter_by(user_id = current_user.id).group_by(Item.status, Item.type).all()
    # Convert the result to a list of dictionaries, for use for plotly plot's data source
    item_status_data = [dict(result) for result in item_status_data]

    # Creates a figure with plotly express using the item status data
    figure = px.bar(item_status_data, x = 'status', y = 'count', color = 'type', barmode = 'group')
    # Converts data from plotly express to JSON for the client side
    graphJSON = json.dumps(figure, cls = plotly.utils.PlotlyJSONEncoder)

    return render_template('items_by_status.html', 
        title = 'Items by Status', graphJSON = graphJSON
    )

