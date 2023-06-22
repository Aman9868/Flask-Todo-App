from app import app,db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo,Email
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __init__(self, user_id, description):
        self.user_id = user_id
        self.description = description

# User model
class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), unique=True, nullable=False)
     email = db.Column(db.String(120), unique=True, nullable=False)
     password = db.Column(db.String(120), nullable=False)

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')