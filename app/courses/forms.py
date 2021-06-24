from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_login import current_user

from app import PRIORITY_OPTIONS, STATUS_OPTIONS
from app.forms import MultiCheckboxField
from app.models import Tag

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


class CourseAddForm(CourseEditForm):
    '''Form for creating a new course, including assigning tags'''

    def __init__(self, *args, **kwargs):
        super(CourseAddForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.filter_by(user_id=current_user.id)]

    tags = MultiCheckboxField('Tags', coerce=int)
    submit = SubmitField('Add course')
