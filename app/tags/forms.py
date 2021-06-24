from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import HiddenInput

from app.models import Tag

class TagEditForm(FlaskForm):
    '''Form for editing an existing tag'''
    id = IntegerField(widget=HiddenInput())
    name = StringField('Tag name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Save changes')

    def validate_name(form, field):
        if field.raw_data:
            # Make all tag names lowercase and remove trailing & leading whitespace
            # for simplicity of keeping them unique
            field.data = field.data.lower()
            field.data = field.data.strip()

            # Check if tag already exists and whether it's not the one being saved
            existing_tag = Tag.query.filter_by(name=field.data).first()
            if existing_tag:
                # If the tag already exists, but it's not this one
                # get the user to save as a different name to avoid duplication
                if existing_tag.id != form.id.data:
                    raise ValidationError('Tag name must be unique')
        else:
            raise ValidationError('Tag name cannot be blank')

class TagAddForm(FlaskForm):
    '''Form for creating a new tag'''
    name = StringField('Tag name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Add tag')

    def validate_name(form, field):
        if field.raw_data:
            # Make all tag names lowercase and remove trailing & leading whitespace
            # for simplicity of keeping them unique
            field.data = field.data.lower()
            field.data = field.data.strip()

            # Check if the tag already exists - if so, it shouldn't be added
            existing_tag = Tag.query.filter_by(name=field.data).first()
            if existing_tag:
                raise ValidationError('Tag name must be unique')
        else:
            raise ValidationError('Tag name cannot be blank')