from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms import validators
from wtforms.validators import DataRequired, Length

from app import priority_options, status_options

class CourseEditForm(FlaskForm):
    ''' Form for editing an existing course '''
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    url = StringField('URL', validators=[Length(max=200)])
    status = SelectField('Status', choices=status_options)
    priority = SelectField('Priority', choices=priority_options)
    next_steps = TextAreaField('Next steps')
    barriers = TextAreaField('Barriers')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save changes')