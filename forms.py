from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password1 = PasswordField('password1', validators=[DataRequired(), Length(min=8, max=25, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password1', message="Password must match")])
    submit = SubmitField('submit', validators=[DataRequired()])
