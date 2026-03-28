from flask import render_template
import os
from flask_cors import CORS
from flask import Blueprint, request, jsonify, json
import uuid

main = Blueprint('main', __name__)
CORS(app=main)

get_products = []

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, 'user.json')
PRODUCTS_FILE = os.path.join(BASE_DIR, 'products.json')

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, 'r') as f:
        return json.load(f)
    
def save_products(products_to_save):
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products_to_save, f, indent=4)

        
@main.route('/api') # Principal Route.
def home():
    return render_template('index.html')

@main.route('/logout/', methods=['POST']) # Route to log out of account.
def logout():
    return {"message": "Logout Successfully!"}, 200

@main.route('/api/products/', methods=['GET']) # Route to see the products.
def products():
    products_list = load_products()
    return jsonify(products_list)

@main.route('/api/products/<product_id>/', methods=['GET']) # Route to access the product by UUID.
def productsId(product_id):
    products_list = load_products()

    for p in products_list:
        if p['id'] == product_id:
            return p
    return {"message": "Product not found."}, 404

@main.route('/api/products/add/', methods=['POST']) # Route to add products.
def add_product():
    products_list = load_products()

    productsId = str(uuid.uuid4())
    newItem = {"description": "TV Smart 4K Oled", "id": productsId, "name": "Tv Smart", "price": 4589.0}

    products_list.append(newItem)
    save_products(products_list)
    
    return {"message": "Saved products successfully!"}, 200

@main.route('/api/products/update/<product_id>/', methods=['PUT']) # Route to update products by UUID.
def update_product(product_id):
    product_list = load_products()

    newName = request.json.get('name')
    newDescription = request.json.get('description')
    newPrice = request.json.get('price')

    updateProduct = next((p for p in product_list if p ['id'] == product_id), None)

    if updateProduct:
        updateProduct['nome'] = newName
        updateProduct['description'] = newDescription
        updateProduct['price'] = newPrice
        save_products(product_list)
        return {"message": "Product updated sucessfully!"}, 200

    return {"message": "Product not found."}, 404

@main.route('/api/products/delete/<product_id>', methods=['DELETE'])
def delete_produt(product_id):
   products_list = load_products()

   removeProduct = next((p for p in products_list if p['id'] == product_id), None)

   if removeProduct:
       products_list.remove(removeProduct)
       save_products(products_list)
       return {"message": "Product deleted sucesfully!"}, 200

   return {"message": "Product not found by UUID."}, 404

@main.route('/api/market/search/', methods=['GET'])
def search_products():
    products_list = load_products()
    query = request.args.get('q', '').lower()

    if query:
        results = [
            p for p in products_list
            if query in p['name'].lower() or query in p['description'].lower()
        ]
        return jsonify(results)

    return render_template('index.html')