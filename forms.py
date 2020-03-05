from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password1 = PasswordField('password1', validators=[DataRequired(), Length(min=8, max=25, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password1', message="Password must match")])
    submit = SubmitField('submit', validators=[DataRequired()])


class LoginForm(FlaskForm):
    login_email = StringField('email', validators=[DataRequired(), Email()])
    login_password = PasswordField('password', validators=[DataRequired(message="Password field is required")])
    submit = SubmitField('submit', validators=[DataRequired()])


class CreateTable(FlaskForm):
    tablenumber = TextField('tablenumber', validators=[DataRequired()])
    submit = SubmitField('submit', validators=[DataRequired()])
