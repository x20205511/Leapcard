from typing import DefaultDict
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User, Card


class LogForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegForm(FlaskForm):
    firstname = StringField('FirstName', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=2, max=20)])
    #username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
         user = User.query.filter_by(email=email.data).first()
         if user:
            raise ValidationError('Email already exists. Please use a different email!')

#For application process of the card, we will create a class and declare the paramaters.
class CardForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    cardnum = StringField('Card Number')
    balance = IntegerField('Balance', validators=[DataRequired()])
    submit = SubmitField('Apply')

#To update/remove card balance for the user
class UpdateForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    add_submit = SubmitField('Add')
    withdraw_submit = SubmitField('Withdraw')
