

class ErrorResponse():
    INVALID_PAYLOAD = {
        "response_code":"INVALID_PAYLOAD",
        "response_title":"Request could not be processed. The payload sent is invalid."
    }
    
    DUPLICATE_USERNAME = {
        "response_code":"DUPLICATE_USERNAME",
        "response_title":"Request could not be processed. username already in use"
    }
    
    UNAUTHORIZE_ACCESS = {
        "response_code":"UNAUTHORIZE_ACCESS",
        "response_title":"Request could not be processed. only admin can handle this request"
    }
    
    DUPLICATE_PRODUCT = {
        "response_code":"DUPLICATE_PRODUCT",
        "response_title":"product already added"
    }
    
    TOKEN_MISSING = {
        "response_code":"TOKEN_MISSING",
        "response_title":"Request could not be processed. Token is missing!"
    }
    
    TOKEN_EXPIRED = {
        "response_code":"TOKEN_EXPIRED",
        "response_title":"Request could not be processed. Token has expired!"
    }
    
    INVALID_TOKEN = {
        "response_code":"TOKEN_EXPIRED",
        "response_title":"Request could not be processed. Invalid token!"
    }
    
    PRODUCT_NOT_FOUND = {
        "response_code":"PRODUCT_NOT_FOUND",
        "response_title":"Request could not be processed. Product not found!"
    }
    
    FAILED_DELETE_PRODUCT = {
        "response_code":"FAILED_DELETE_PRODUCT",
        "response_title":"failed to delete product"
    }