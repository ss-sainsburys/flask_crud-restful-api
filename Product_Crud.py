from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db=SQLAlchemy(app)

#Init Marshmellow
ma =Marshmallow(app)

#Create Product model

class Product(db.Model):
  id =db.Column(db.Integer,primary_key =True)
  name=db.Column(db.String(100),unique = True)
  description =db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self,name,description,price,qty):
    self.name = name
    self.description = description
    self.price =price
    self.qty = qty

class ProductSchema(ma.Schema):
  class Meta:
    fields =('id','description','price','qty')

product_schema = ProductSchema()
products_schema =ProductSchema(many =True)
#create Product
@app.route('/Product',methods =['POST'])

def add_product():
    name =request.json['name']
    description =request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

#Fetch  specific ProductSchema

@app.route('/Product/<id>',methods =['GET'])

def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#Fetch all product
@app.route('/Product',methods=['GET'])

def get_all_product():
    all_product =Product.query.all()
    result = products_schema.dump(all_product)
    return jsonify(result.data)

#Delete specific product row
@app.route('/Product/<id>',methods =['DELETE'])

def delete_product(id):
    delete_product =Product.query.get(id)
    db.session.delete(delete_product)
    db.session.commit()
    return product_schema.jsonify(delete_product)

#Modify the product
@app.route('/Product/<id>',methods =['PUT'])

def modify_product(id):
    modified_product = Product.query.get(id)

    name = request.json['name']
    description =request.json['description']
    price = request.json['price']
    qty = request.json['qty']


    modified_product.name =name
    modified_product.description =description
    modified_product.price = price
    modified_product.qty = qty

    db.session.commit()

    return product_schema.jsonify(modified_new_product)

if __name__ =='__main__':
    app.run(debug =True)
