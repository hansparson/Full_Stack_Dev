from flask import jsonify, current_app as app
from datetime import datetime, timedelta
import jwt
import hashlib
from functools import wraps
from core.config import Config
from core.response import ErrorResponse

class Authentification(object):
    def __init__(self, params='', headers='', payload=''):
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
        
        
    def login_required(self):
        token = None
        if 'Authorization' in self.headers:
            token = self.headers['Authorization'].split(' ')[1]

        if not token:
            print(ErrorResponse.TOKEN_MISSING, 401)
            return False, ErrorResponse.TOKEN_MISSING, 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            data_user = dict(
               current_user = data['sub'],
               type_user = data['type_user'] 
            )
        except jwt.ExpiredSignatureError:
            print(ErrorResponse.TOKEN_EXPIRED, 401)
            return False, ErrorResponse.TOKEN_EXPIRED, 401
        except jwt.InvalidTokenError:
            print(ErrorResponse.INVALID_TOKEN, 401)
            return False, ErrorResponse.INVALID_TOKEN, 401

        return True, data_user, 200

    
    def hashing_password(username, password):
        salt = hashlib.sha256(Config.SECRET_KEY.encode()).hexdigest()[:16]
        encrypt_str = '{}||{}'.format(username, password)
        salted_str = '{}||{}'.format(encrypt_str, salt)
        hashed_str = hashlib.sha256(salted_str.encode()).hexdigest()
        return hashed_str