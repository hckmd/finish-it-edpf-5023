import json

from flask import render_template
from flask_login import login_required, current_user
import plotly
import plotly.express as px
from sqlalchemy import func

from app import db, STATUS_OPTIONS, ITEM_TYPES
from app.reports import bp
from app.models import Item, User, Tag
from app.admin.decorators import admin_required

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('reports.html', title = 'Reports')

@bp.get('/item_status')
@login_required
def item_status_view():
    return render_template('items_by_status.html', title = 'Items by Status')

@bp.get('/item_status_data')
@login_required
def item_status_data():
    # Queries the Items table to get the number of items for status and type
    item_status_data = db.session.query(
        Item.status, Item.type, func.count(Item.id).label('count')
        ).filter_by(user_id = current_user.id).group_by(Item.status, Item.type).all()
    # Convert the result to a list of dictionaries, for use for plotly plot's data source
    item_status_data = [dict(result) for result in item_status_data]

    # Create entries in the data for status options and types that dont result from the data
    item_types = ['book','course']
    for status in STATUS_OPTIONS:
        for item_type in item_types:
            existing_data = [result for result in item_status_data 
                if result['status'] == status and result['type'] == item_type]
            if len(existing_data) == 0:
                missing_data = {'status': status, 'type': item_type, 'count': 0}
                item_status_data.append(missing_data)

    # Creates a figure with plotly express using the item status data
    figure = px.bar(item_status_data, 
        x = 'status', y = 'count', color = 'type', barmode = 'group',
        labels = {'status': 'Status', 'count': 'Number of items', 'type': 'Type'}
    )
    # Converts data from plotly express to JSON for the client side
    graphJSON = json.dumps(figure, cls = plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@bp.get('/user_type')
@admin_required
@login_required
def user_type_view():
    return render_template('users_by_type.html', title = 'Users by Type')

@bp.get('/user_type_data')
@admin_required
@login_required
def user_type_data():
    # Queries the Items table to get the number of users that are admin and non-admin
    user_type_data = db.session.query(
        User.is_administrator.label('type'), func.count(User.id).label('count')
        ).group_by(User.is_administrator).all()
    # Convert the result to a list of dictionaries, for use for plotly plot's data source
    user_type_data = [dict(result) for result in user_type_data]

    # Change the values of the type from False or True to more clearly labelled value
    for row in user_type_data:
        if row['type'] == False:
            row['type'] = 'Normal user'
        else:
            row['type'] = 'Admin'

    # Creates a figure with plotly express using the item status data
    figure = px.bar(user_type_data, 
        x = 'type', y = 'count',
        labels = {'type': 'User type', 'count': 'Number of users'}
    )
    # Converts data from plotly express to JSON for the client side
    graphJSON = json.dumps(figure, cls = plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@bp.get('/tag_items')
@login_required
def tag_items_view():
    return render_template('tag_items.html', title = 'Number of Items per Tag')

@bp.get('/tag_items_data')
@login_required
def tag_items_data():
    tag_items = []
    
    tags = Tag.query.filter_by(user_id = current_user.id)  
    for tag in tags:
        for item_type in ITEM_TYPES:
            number_of_items = len([item for item in tag.items if item.type == item_type])
            tag_data = { 'Tag': tag.name, 'Item Type': item_type, 'Number of items': number_of_items }
            tag_items.append(tag_data)

    # Creates a figure with plotly express using the tag and items data
    figure = px.bar(tag_items, x = 'Tag', y = 'Number of items', color = 'Item Type', barmode = 'group')
    
    # Converts data from plotly express to JSON for the client side
    graphJSON = json.dumps(figure, cls = plotly.utils.PlotlyJSONEncoder)
    return graphJSON