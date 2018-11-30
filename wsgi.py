import os
import logging
# logging.warn(os.environ["DUMMY"])

from flask import Flask, request, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema


class Productview(ModelView):
    can_view_details = True
    can_create = False
    can_edit = False
    can_delete = False
    page_size = 50

admin = Admin(app, name='Back-office', template_mode='bootstrap3')
admin.add_view(Productview(Product, db.session)) # `Product` needs to be imported before

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    #return products_schema.jsonify(products)
    return render_template('home.html', products=products)

@app.route('/products', methods=['POST'])
def add_product():
    content = request.get_json("name")
    product = Product()
    product.name = content["name"]
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<int:id>')
def get_product(id):
    product = db.session.query(Product).get(id)
    if not product:
        return 'Product does not exist', 404
    # return product_schema.jsonify(product)
    return render_template('product_detail.html', product=product)

@app.route('/products/<int:id>', methods=['PATCH'])
def update_product(id):
    content = request.get_json("name")
    product = db.session.query(Product).get(id)
    if not product:
        return 'Product does not exist', 404
    product.name = content["name"]
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.query(Product).get(id)
    if not product:
        return 'Product does not exist', 404
    db.session.delete(product)
    db.session.commit()
    return f'Product with id {id} deleted', 200
