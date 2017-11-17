from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Email, Length, EqualTo,
                                ValidationError)


from models import User


def email_exists(form, field):
    """This checks the database to see if a user's email already exists
    in the database. If so a ValidationError is raised."""
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    """This is the form user's complete to login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])


class TacoForm(Form):
    """This gets the user's taco choices."""
    protein = StringField('Protein', validators=[DataRequired()])
    shell = StringField('Shell', validators=[DataRequired()])
    cheese = StringField('Cheese')
    extras = StringField('Extras')
