from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
app = Flask(__name__)
SECRET_KEY=os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Todo App/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = SECRET_KEY  # Replace with your own secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  #
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
from app import routes,models
with app.app_context():
    db.create_all()