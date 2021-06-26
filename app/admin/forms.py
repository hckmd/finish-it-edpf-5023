from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.widgets import HiddenInput

from app.models import User

class UserAddForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm password:', validators=[DataRequired()])
    is_administrator = BooleanField('Is administrator?')
    submit = SubmitField('Add user')

    def validate_username(form, field):
        # Check if the username already exists
        user = User.query.filter_by(username = field.data).first()
        if user != None:
            raise ValidationError('User name must be unique.')

    def validate_email(form, field):
        # Check if a user with the email already exists
        user = User.query.filter_by(email = field.data).first()
        if user != None:
            raise ValidationError('Email address must be unique.') 
        
class UserEditDetailsForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    is_administrator = BooleanField('Is administrator?')
    submit = SubmitField('Save changes')

    def validate_username(form, field):
        # Check if the username already exists and doesn't belong to this user
        user = User.query.filter_by(username = field.data).first()
        if user != None and user.id != form.id.data:
            raise ValidationError('User name must be unique.')

    def validate_email(form, field):
        # Check if a user with the email already exists and it's not this one
        user = User.query.filter_by(email = field.data).first()
        if user != None and user.id != form.id.data:
            raise ValidationError('Email address must be unique.') 
    
class UserChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm password:', validators=[DataRequired()])
    submit = SubmitField('Change password')