from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SelectField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.fields.datetime import DateField
from app.models import User

class NewArtist(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    about_me = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField("Create")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class VenueForm(FlaskForm):
    name = StringField('Venue Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    size = IntegerField('Size', validators=[DataRequired()])
    submit = SubmitField('Create New Venue')


class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    date = DateField('Date and Time', validators=[DataRequired()])
    venue = SelectField('Venue', coerce=int, validators=[DataRequired()])
    artists = SelectMultipleField('Artists', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create New Event')
