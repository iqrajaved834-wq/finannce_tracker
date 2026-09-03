from functools import wraps
from flask import session, jsonify


def login_required(f):

    @wraps(f)
    def decorator_function(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({
                "error": "Authentication required! Please login."
            }), 401

        return f(*args, **kwargs)

    return decorator_function

#wraps=used to  save the actual information about the function,session+used to save all the login info,jsonify=sent response in json format
# we define our decorator def decorator_name(f)
# wraps(f)    
#set the decorator function for our custom decorator....that will check id in session ,if not found it will give json error,if found it wiill run the origional function on which the decorator is appliesa and after that is wuill return the decorated function