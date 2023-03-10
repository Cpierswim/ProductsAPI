from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields, ValidationError;
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
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory_quantity = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f'ID: {self.id} Name: {self.name} {self.description} {self.price} {self.inventory_quantity} {self.img_url}'

# Schemas
class ProductSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    inventory_quantity = fields.Integer(required=True)
    img_url = fields.String()

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'inventory_quantity', 'img_url')

    @post_load
    def create_product(self, data, **kwargs):
        return Products(**data)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Resources
class ProductListResoucre(Resource):
    def get():
        all_produts = Products.query.all()
        return products_schema.dump(all_produts), 200

    def post(self):
        try:
            add_product = product_schema.load(request.get_json())
            db.session.add(add_product)
            db.session.commit()
            return product_schema.dump(add_product), 201
        except ValidationError as error:
            return error.messages, 400
        
class ProductResource(Resource):
    def get(self, product_id):
        return product_schema.dump(Products.query.get_or_404(product_id)), 200
    
    def put(self, product_id):
        product_from_db = Products.query.get_or_404(product_id)
        if 'name' in request.json:
            product_from_db.name = request.json['name']
        if 'description' in request.json:
            product_from_db.description = request.json['description']
        if 'price' in request.json:
            product_from_db.price = request.json['price']
        if 'inventory_quantity' in request.json:
            product_from_db.inventory_quantity = request.json['inventory_quantity']
        if 'img_url' in request.json:
            product_from_db.img_url = request.json['img_url']
        db.session.commit()
        return product_schema.dump(product_from_db), 201
    
    def delete(self, product_id):
        product_from_db = Products.query.get_or_404(product_id)
        db.session.delete(product_from_db)
        db.session.commit()
        return '', 204

# Routes
api.add_resource(ProductListResoucre, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:product_id>')