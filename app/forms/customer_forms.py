from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, TextField, FileField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, Optional, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    first_name = StringField(validators=[InputRequired()])
    last_name = StringField(validators=[InputRequired()])
    telephone = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(),EqualTo('confirm_password'), Length(min=8, max=64)])
    confirm_password = PasswordField(validators=[InputRequired()])
    street = StringField(validators=[InputRequired()])
    town = StringField(validators=[InputRequired()])
    parish = StringField(validators=[InputRequired()])

    username = TextField('Username',validators=[DataRequired()])   
    password = PasswordField('Password',validators=[DataRequired()])   
    fullname = TextField('Fullname',validators=[DataRequired()])   
    email = TextField('Email',validators=[DataRequired()])   
    location = TextField('Location',validators=[DataRequired()])   
    biography =TextAreaField('Biography',validators=[DataRequired()])   
    photo = FileField('Photo',validators=[FileRequired(), FileAllowed(['jpg','png'])])


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])


class UpdateAccountForm(FlaskForm):
    first_name = StringField(validators=[InputRequired()])
    last_name = StringField(validators=[InputRequired()])
    telephone = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[Optional(),EqualTo('confirm_password'), Length(min=8, max=64)])
    confirm_password = PasswordField(validators=[Optional()])