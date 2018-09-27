from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import Employee
from flask import flash,render_template

class RegisterationForm(FlaskForm):
    #Form to create new account
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    first_name = StringField('First Name',validators = [DataRequired()])
    last_name = StringField('Last Name',validators = [DataRequired()])
    password = PasswordField('Password',validators= [DataRequired(),EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self,field):
        if Employee.query.filter_by(email=field.data).first():
            print('in validate email----------------------------------------')


    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            print('in validate username----------------------------------------')

class LoginForm(FlaskForm):
    #create login Form
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
