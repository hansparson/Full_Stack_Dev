from marshmallow import (
    ValidationError
)
import json
from core.response import ErrorResponse
from validation.schema_validation import AddProducts
from utils.generator import GeneratorUtils
from validation.authentification import Authentification
from models.products import Products, db_product_query

class ProductsServices(object):
    def __init__(self, params='', headers='', payload=''):
        self.headers = headers
        self.payload = payload
        self.params = params
    
    def add_products(self):
        
        # login required
        bolean, token_resp, status_code = Authentification(headers=self.headers).login_required()
        if bolean != True:
            return token_resp, status_code
        
        # check schema
        try:
            AddProducts().load(self.payload)
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
        
        #Check Admin
        if token_resp['type_user'] != "ADMIN":
            response = ErrorResponse.UNAUTHORIZE_ACCESS
            response = {
                "response_code": response["response_code"],
                "response_title": response["response_title"]
            }
            return response, 400
        
        product_data = dict(
            item_id = GeneratorUtils._generate_user_id(self),
            item_name = self.payload['item_name'],
            quantity = self.payload['quantity'],
            description = self.payload['description']
        )
        
        add_product = Products(**product_data).save()
        if add_product == None:
            response = ErrorResponse.DUPLICATE_PRODUCT
            return response, 400
        
        response = {
                "response_code": "SUCCESS",
                "response_title": "success add new item",
                "response_data": {
                    "item_name": self.payload['item_name'],
                    "quantity": self.payload['quantity'],
                    "description": self.payload['description']
                }
            }
        
        return response, 200
    
    def update_products(self):
        # login required
        bolean, token_resp, status_code = Authentification(headers=self.headers).login_required()
        if bolean != True:
            print(token_resp, status_code)
            return token_resp, status_code
        
        # check schema
        try:
            AddProducts().load(self.payload)
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
            print(token_resp, status_code)
            return response, 400
        
        #Check Admin
        if token_resp['type_user'] != "ADMIN":
            response = ErrorResponse.UNAUTHORIZE_ACCESS
            response = {
                "response_code": response["response_code"],
                "response_title": response["response_title"]
            }
            print(token_resp, status_code)
            return response, 400
        
        # Querry Products
        product = db_product_query.get_product_item_name(self.params['item_name'])
        if product is None:
            response = ErrorResponse.PRODUCT_NOT_FOUND
            response = {
                "response_code": response["response_code"],
                "response_title": response["response_title"]
            }
            print(token_resp, status_code)
            return response, 401
        
        product_data = dict(
            item_query_name = self.params['item_name'],
            item_name = self.payload['item_name'],
            quantity = self.payload['quantity'],
            description = self.payload['description']
        )
        
        add_product = db_product_query.update_product(product_data)
        if add_product == None:
            response = ErrorResponse.DUPLICATE_PRODUCT
            print(token_resp, status_code)
            return response, 400
        
        response = {
                "response_code": "SUCCESS",
                "response_title": "success update item {}".format(self.payload['item_name']),
                "response_data": {
                    "item_name": self.payload['item_name'],
                    "quantity": self.payload['quantity'],
                    "description": self.payload['description']
                }
            }
        print(token_resp, status_code)
        return response, 200
    
    def delete_product(self):
        # login required
        bolean, token_resp, status_code = Authentification(headers=self.headers).login_required()
        if bolean != True:
            print(token_resp, status_code)
            return token_resp, status_code
        
        #Check Admin
        if token_resp['type_user'] != "ADMIN":
            response = ErrorResponse.UNAUTHORIZE_ACCESS
            response = {
                "response_code": response["response_code"],
                "response_title": response["response_title"]
            }
            print(token_resp, status_code)
            return response, 400
        
        # Querry Products
        product = db_product_query.get_product_item_name(self.params['item_name'])
        if product is None:
            response = ErrorResponse.PRODUCT_NOT_FOUND
            response = {
                "response_code": response["response_code"],
                "response_title": response["response_title"]
            }
            print(token_resp, status_code)
            return response, 401

        # Delete product on DB
        try :
            db_product_query.delete_product(self.params['item_name'])
        except : 
            response = ErrorResponse.FAILED_DELETE_PRODUCT
            print(token_resp, status_code)
            return response, 400
        
        response = {
                "response_code": "SUCCESS",
                "response_title": "Success Delete item {}".format(self.params['item_name']),
                "response_data": {
                }
            }
        
        return response, 200

    def view_all_item(self):
        # login required
        bolean, token_resp, status_code = Authentification(headers=self.headers).login_required()
        if bolean != True:
            print(token_resp, status_code)
            return token_resp, status_code
        
        products = db_product_query.get_all_item()
        product_data = []
        count = 0
        for product in products:
            product_item = {
                'item_name' : product.item_name,
                'quantity' : product.quantity,
                'description' : product.description
            }
            count += 1
            product_data.append(product_item)
        
        response = {
            "response_code": "SUCCESS",
            "response_title": "Success Get All item total {}".format(count),
            "response_data": product_data
        }
        
        return response, 200