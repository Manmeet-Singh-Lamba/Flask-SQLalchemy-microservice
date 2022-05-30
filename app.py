from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# initialize the app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize database
db = SQLAlchemy(app)

#InitialiZe Marshmallow 
ma = Marshmallow(app)

#Product Class/Model 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = True)
    category = db.relationship('Category')
    
    def __init__(self, name, description, price, qty, category_id):
        self.name = name
        self.description = description
        self.price =price
        self.qty = qty
        self.category_id = category_id

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(30), unique = True)

# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty', 'category_id')

#Initialize schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/product', methods = ['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    category_id = request.json['category_id']

    new_product = Product(name, description, price, qty, category_id)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get all products
@app.route('/product', methods =['GET'])
def get_products():
    all_products = Product.query.all()
    results = products_schema.dump(all_products)
   # return products_schema.jsonify(all_products)  # this is correct too
    return jsonify(results)

# Get single product
@app.route('/product/<id>', methods =['GET'])
def get_single_products(id):
    result = Product.query.get(id)
    return product_schema.jsonify(result)  

# Delete single product
@app.route('/product/<id>', methods =['DELETE'])
def delete_single_products(id):
    result = Product.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return product_schema.jsonify(result)  

# Update a Product
@app.route('/product/<id>', methods = ['PUT'])
def update_product(id):
    result = Product.query.get(id)

    result.name = request.json['name']
    result.description = request.json['description']
    result.price = request.json['price']
    result.qty = request.json['qty']
    result.category_id = request.json['category_id']

    db.session.commit()
    return product_schema.jsonify(result)

# Run server
if __name__ == "__main__":
    app.run(debug =True)