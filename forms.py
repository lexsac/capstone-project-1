from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField


class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('E-mail')
    username = StringField('Username')
    password = PasswordField('Password')
    profile_img = StringField('(Optional) Image URL')
    experience_level = StringField('Experience Level')
    location = StringField('Job Location')
    category = StringField('Job Category')
    company = StringField('Company')


class UserEditForm(FlaskForm):
    """Form for editing users."""

    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('E-mail')
    username = StringField('Username')
    password = PasswordField('Password')
    profile_img = StringField('(Optional) Image URL')
    experience_level = StringField('Experience Level')
    location = StringField('Job Location')
    category = StringField('Job Category')
    company = StringField('Company')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username')
    password = PasswordField('Password')
    
