from flask import Blueprint, request
from services.users import UserServices

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/register_new_users', methods=['POST'])
def create_users():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    order_services = UserServices(payload=payload, headers=headers, params=params)
    response, response_code = order_services.create_new_users()
    
    return response, response_code

@users_bp.route('/login', methods=['POST'])
def login():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    order_services = UserServices(payload=payload, headers=headers, params=params)
    response, response_code = order_services.login_users()
    
    return response, response_code