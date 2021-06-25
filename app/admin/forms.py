from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from app.models import User

class UserAddForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm password:', validators=[DataRequired()])
    is_administrator = BooleanField()
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
        

