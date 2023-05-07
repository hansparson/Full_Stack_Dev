from flask import Blueprint, request
from services.products import ProductsServices

product_bp = Blueprint('products', __name__, url_prefix='/products')

@product_bp.route('/add_products', methods=['POST'])
def add_products():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    order_services = ProductsServices(payload=payload, headers=headers, params=params)
    response, response_code = order_services.add_products()
    
    return response, response_code

@product_bp.route('/update_products', methods=['POST'])
def update_products():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    order_services = ProductsServices(payload=payload, headers=headers, params=params)
    response, response_code = order_services.update_products()
    
    return response, response_code

@product_bp.route('/delete_product', methods=['DELETE'])
def delete_product():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    order_services = ProductsServices(payload=payload, headers=headers, params=params)
    response, response_code = order_services.delete_product()
    
    return response, response_code

@product_bp.route('/all_products', methods=['GET'])
def all_products():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    order_services = ProductsServices(payload=payload, headers=headers, params=params)
    response, response_code = order_services.view_all_item()
    
    return response, response_code