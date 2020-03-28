
"""
Create database table
"""

#import packages
from shoplte import app
from shoplte import custom_config
from shoplte.models import *
import os

#import data
from shoplte.demo import feeds, trends

#database configuration
app.config["SQLALCHEMY_DATA=BASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#create database once
try:
    with app.app_context():
        db.create_all()
        print("Database and Tables created successfully")
except Exception as e:
    print(f"Could not create database: {e}")