from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///theatre.db'
db = SQLAlchemy(app)

from app.routes import *

with app.app_context():
    db.create_all()