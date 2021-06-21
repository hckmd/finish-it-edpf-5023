from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

from app import priority_options, status_options
from app.models import Tag
from app.forms import MultiCheckboxField

class BookEditForm(FlaskForm):
    ''' Form for editing an existing book '''
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    authors = StringField('Authors', validators=[Length(max=100)])
    status = SelectField('Status', choices=status_options)
    priority = SelectField('Priority', choices=priority_options)
    next_steps = TextAreaField('Next steps')
    barriers = TextAreaField('Barriers')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save changes')

class BookAddForm(BookEditForm):
    '''Form for creating a new book, including assigning tags'''

    def __init__(self, *args, **kwargs):
        super(BookAddForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    tags = MultiCheckboxField('Tags', coerce=int,)
    submit = SubmitField('Add book')
