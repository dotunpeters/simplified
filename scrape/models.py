
"""
Create database schema
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    stars = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    seller = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)