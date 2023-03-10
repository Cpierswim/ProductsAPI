from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    discription = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory_quantity = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f'ID: {self.id} Name: {self.name} {self.discription} {self.price} {self.inventory_quantity} {self.img_url}'

# Schemas



# Resources



# Routes
