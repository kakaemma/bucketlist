from functools import wraps
from models.users import UserModal
import datetime
import jwt
# from api.bucket import app
from api.bucket import *


#
# def get_token():
#     """ This methods gets the token from the headers"""
#     try:
#         auth_token = request.headers.get('Authorization')
#         token = auth_token.split(" ")[1]
#         return token
#     except Exception as e:
#         # log error
#         return e



def method_to_be_returned(func, *args, **kwargs):
    """ This method selects which function to return"""
    try:
        if len(args) == 0 and len(kwargs) == 0:
            return func()
        else:
            return func (*args, **kwargs)
    except Exception as exc:
        response = jsonify({'Failed with Exception': exc})
        response.status_code = 500
        return response


def validate_content_type(f):
    """ This method checks whether the content-type is application/json"""
    @wraps(f)
    def decorated_method(*args, **kwargs):
        # log errors here
        if request.headers.get('content-type') != 'application/json':

           response = jsonify({
               'Error': 'Content-Type not specified as application/json'
           })
           response.status_code = 400
           return response

        return method_to_be_returned(f,  *args, **kwargs)
    return decorated_method


# def validate_token(f):
#     @wraps(f)
#     def decorated_method(*args, **kwargs):
#         token = get_token()
#         if token is None:
#             response = jsonify({
#                 'Error': 'There is no access token'
#             })
#             response.status_code = 401
#             return response
#         try:
#             user_id = decode_auth_token(token)
#             user = UserModal.get_user_by_id(user_id)
#             if user is None:
#                 response = jsonify({
#                     'status': 'mismatching or wrong token'
#                 })
#                 response.status_code = 401
#                 return response
#
#         except Exception as exc:
#             response = jsonify({
#                 'Failed with exception': exc
#             })
#             response.status_code = 500
#
#         return method_to_be_returned(f, *args, **kwargs)
#     return decorated_method
#
#
# def encode_auth_token(user_id):
#     """
#     This method encodes the Authorisation token
#     :param user_id:
#     :return:
#     """
#     try:
#
#         payload = {
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
#             'iat': datetime.datetime.utcnow(),
#             'sub': user_id
#         }
#
#         auth_token = jwt.encode(
#             payload,
#             "app.config.get('SECRET_KEY')",
#             algorithm='HS256')
#         return auth_token
#
#     except Exception as exc:
#         #logg errors here
#         return exc
#
#
# def decode_auth_token(token):
#     """
#     Decodes the authorization token
#     :param token:
#     :return:
#     """
#     try:
#         payload = jwt.decode(token, app.config.get('SECRET_KEY'))
#         user = payload['sub']
#         return user
#     except jwt.ExpiredSignature:
#         return 'Token expired please login again'
#     except jwt.InvalidTokenError:
#         return 'Invalid token. Please login again \n'