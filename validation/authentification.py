from flask import jsonify, current_app as app
from datetime import datetime, timedelta
import jwt
import hashlib
from functools import wraps
from core.config import Config

class Authentification(object):
    
    def __init__(self, params='', headers='', payload='',):
        self.headers = headers
        self.payload = payload
        self.params = params
        
        
    def generate_token(self, user_id, type_user):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id,
                'type_user': type_user
            }
            token = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return token
        except Exception as e:
            return str(e)
        
        
    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'Authorization' in self.headers:
                token = self.headers['Authorization'].split(' ')[1]

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                current_user = data['sub']
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated
    
    def hashing_password(username, password):
        salt = hashlib.sha256(Config.SECRET_KEY.encode()).hexdigest()[:16]
        encrypt_str = '{}||{}'.format(username, password)
        salted_str = '{}||{}'.format(encrypt_str, salt)
        hashed_str = hashlib.sha256(salted_str.encode()).hexdigest()
        return hashed_str