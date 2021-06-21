from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Tag

class TagAddForm(FlaskForm):
    '''Form for creating a new tag'''
    name = StringField('Tag name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Add tag')

    def validate_name(form, field):
        if field.raw_data:
            # Make all tag names lowercase for simplicity of keeping them unique
            field.data = field.data.lower()
            tag_name = Tag.query.filter_by(name=field.data).first()
            if tag_name:
                raise ValidationError('Tag name must be unique')
        else:
            raise ValidationError('Tag name cannot be blank')