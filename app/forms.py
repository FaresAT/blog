from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Register')

    # validate_<NAME> creates custom validators that are invoked alongside normal validators for FlaskForms
    def validate_username(self, username):
        user_check = User.query.filter_by(username=username.data).first()

        # if the username is already taken
        if user_check is not None:
            raise ValidationError("Username already taken! Please pick another username.")

    def validate_email(self, email):
        email_check = User.query.filter_by(email=email.data).first()

        # if email is already taken
        if email_check is not None:
            raise ValidationError("Email address is already in use! Please use another email.")
