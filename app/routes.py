from flask import render_template, Blueprint, request, jsonify
from flask_cors import CORS
import uuid
from .models import Product
from . import db

main = Blueprint('main', __name__)
CORS(app=main)

@main.route('/')
def home():
    return render_template('login.html')

@main.route('/seller')
def seller_page():
    return render_template('seller.html')

@main.route('/customer')
def customer_page():
    return render_template('customer.html')

# products routes, using SQLAlchemy to interact with the database

@main.route('/api/products/', methods=['GET'])
def get_all_products():
    products_list = Product.query.all()
    
    results = [
        {"id": p.id, "name": p.name, "description": p.description, "price": p.price} 
        for p in products_list
    ]
    return jsonify(results)

@main.route('/api/products/<product_id>/', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price
        })
    return {"message": "Product not found."}, 404

@main.route('/api/products/add/', methods=['POST'])
def add_product():
    data = request.json
    
    new_item = Product(
        id=str(uuid.uuid4()),
        name=data.get('name', 'Produto Sem Nome'),
        description=data.get('description', ''),
        price=data.get('price', 0.0)
    )

    db.session.add(new_item)
    db.session.commit()
    
    return {"message": "Saved product to database successfully!"}, 200

@main.route('/api/products/update/<product_id>/', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return {"message": "Product not found."}, 404

    data = request.json
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)

    db.session.commit()
    return {"message": "Product updated successfully!"}, 200

@main.route('/api/products/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully!"}, 200

    return {"message": "Product not found."}, 404

@main.route('/api/market/search/', methods=['GET'])
def search_products():
    query = request.args.get('q', '').lower()
    
    results = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) | 
        (Product.description.ilike(f'%{query}%'))
    ).all()

    formatted_results = [
        {"id": p.id, "name": p.name, "description": p.description, "price": p.price} 
        for p in results
    ]
    
    return jsonify(formatted_results)