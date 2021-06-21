from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

from app import priority_options, status_options

class BookEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    authors = StringField('Authors', validators=[Length(max=100)])
    status = SelectField('Status', choices=status_options)
    priority = SelectField('Priority', choices=priority_options)
    next_steps = TextAreaField('Next steps')
    barriers = TextAreaField('Barriers')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save changes')
