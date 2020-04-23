
"""
Application package.
"""

#import packages
from flask import Flask
from flask_session import Session
from tempfile import mkdtemp
from simplified.model import *
import os

app = Flask(__name__)

#heroku port
port = int(os.environ.get("PORT", 5000))

#session configuration
app.config["DEBUG"] = True
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#create user session
Session(app)

#database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#fixed trending
with app.app_context():
    session_data = {}
    trendings = Products.query.filter(Products.reviews >= 10).order_by(Products.stars.desc()).limit(5).all()

import simplified.routes