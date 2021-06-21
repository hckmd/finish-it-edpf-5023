from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TagAddForm(FlaskForm):
    '''Form for creating a new tag'''
    name = StringField('Tag name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Add tag')