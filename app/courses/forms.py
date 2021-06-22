from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms import validators
from wtforms.validators import DataRequired, Length

from app import PRIORITY_OPTIONS, STATUS_OPTIONS

class CourseEditForm(FlaskForm):
    ''' Form for editing an existing course '''
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    url = StringField('URL', validators=[Length(max=200)])
    status = SelectField('Status', choices=STATUS_OPTIONS)
    priority = SelectField('Priority', choices=PRIORITY_OPTIONS)
    next_steps = TextAreaField('Next steps')
    barriers = TextAreaField('Barriers')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save changes')