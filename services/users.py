from marshmallow import (
    ValidationError
)
import json
from core.response import ErrorResponse
from validation.schema_validation import CreateNewUser, LoginUser
from utils.generator import GeneratorUtils
from validation.authentification import Authentification
from models.users import Users, db_users_query


class UserServices(object):
    
    def __init__(self, params='', headers='', payload=''):
        self.headers = headers
        self.payload = payload
        self.params = params
        
        
    def create_new_users(self):
        
        # Check Schema for CreateUser API
        print(self.payload)
        try:
            CreateNewUser().load(self.payload)
        except ValidationError as error:
            error_message = {}
            for field, messages in error.messages.items():
                error_message[field] = "{}".format(messages)
            response = ErrorResponse.INVALID_PAYLOAD
            response = {
                "response_code": response["response_code"],
                "response_title": response["response_title"],
                "response_desc": error_message
            }
            
            return response, 400
        
        # set all data
        data_user = dict(
            user_id = GeneratorUtils._generate_user_id(self),
            name = self.payload['name'],
            email_address = self.payload['email_address'],
            phone_number = self.payload['phone_number'],
            username = self.payload['username'],
            password = Authentification.hashing_password(self.payload['username'], self.payload['password']),
            type_user = self.payload['type_user']
        )
        # Save order data to database
        add_user = Users(**data_user).save()
        if add_user == None:
            response = ErrorResponse.DUPLICATE_USERNAME
            return response, 400
        
        response = {
                "response_code": "SUCCESS",
                "response_title": "create new user successful",
                "response_data": {
                    "username": self.payload['username'],
                    "type_user": self.payload['type_user']
                }
            }
        
        return response, 200
    
    def login_users(self):
        try:
            LoginUser().load(self.payload)
        except ValidationError as error:
            error_message = {}
            for field, messages in error.messages.items():
                error_message[field] = "{}".format(messages)
            response = ErrorResponse.INVALID_PAYLOAD
            response = {
                "response_code": response["response_code"],
                "response_title": response["response_title"],
                "response_desc": error_message
            }
            
            return response, 400
        
        # Valitadte User :
        user = db_users_query.get_user_data(self.payload['username'])
        if user is None:
            return {'message': 'username not Found'}, 401
        
        #validate Password
        user_password = Authentification.hashing_password(self.payload['username'], self.payload['password'])
        if user_password != user.password:
            return {'message': 'Invalid username or password'}, 401
        
        # Generate Token
        token = Authentification.generate_token(self, self.payload['username'], user.type_user)
        
        response = {
                "response_code": "SUCCESS",
                "response_title": "login successful",
                "response_data": {
                    "token": token
                }
            }
        
        return response, 200