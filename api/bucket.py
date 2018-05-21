from flask import jsonify, request, json, render_template
from api import create_app
from classes.auth import Authenticate
from classes.bucket import Bucket
import datetime
import jwt

app = create_app('TestingEnv')


@app.route('/')
def index():
    """ Index route """
    return render_template('index.html')


@app.route('/auth/register', methods=['POST'])
def register():
    """ Register a user with this endpoint """

    request.get_json(force=True)
    try:
        email = request.json['email']
        name = request.json['name']
        password = request.json['password']
        response = Authenticate.register(name, email, password)
        response = operation_successful(response)

        return response

    except KeyError:
        invalid_keys()


@app.route('/auth/login', methods=['POST'])
def login():
    """End point for login"""

    request.get_json(force=True)
    try:
        email = request.json['email']
        password = request.json['password']
        response = Authenticate.login(email, password)
        print(response)
        response = operation_successful(response)
        return response
    except KeyError:
        invalid_keys()


@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """End point for reset password"""

    request.get_json(force=True)
    try:
        email = request.json['email']
        old_pass = request.json['password']
        new_pass = request.json['new_password']
        response = Authenticate.reset_password(email, old_pass, new_pass)
        response = operation_successful(response)
        return response

    except KeyError:
        invalid_keys()

@app.route('/buckets', methods=['POST'])
def add_bucket():
    request.get_json(force=True)
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            name = request.json['name']
            desc = request.json['desc']
            response = Bucket.add_bucket(name, desc, user_id)
            response = operation_successful(response)
            return response

        else:
            return invalid_token()

    except KeyError:
        invalid_keys()


@app.route('/auth/logout', methods=['POST'])
def logout():
    pass


def invalid_keys():
    """
    Handles invalid keys
    :return: 
    """
    response = jsonify({'Error': 'Invalid keys'})
    response.status_code = 400
    return response


def operation_successful(response):
    """
    Handles successful execution of operations
    :param response: 
    :return: 
    """
    if response.status_code == 201:
        data = json.loads(response.data.decode())
        data['token'] = encode_auth_token(data['id']).decode()
        response = jsonify(data)
        response.status_code = 201
    return response


def invalid_token():
    """
    Handles invalid tokens
    :return: String
    """
    response = jsonify({'Error': 'Invalid Token '})
    response.status_code = 400
    return response


def encode_auth_token(user_id):
    """
    Generates the auth token
    :param user_id: 
    :return: String
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id

        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256')
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the authorisation token
    :param auth_token: 
    :return: integer | String
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignature:
        response = jsonify({'Signature expired. ': 'Please login again'})
        response.status_code = 401
        return response

    except jwt.InvalidTokenError:
        response = jsonify({'Error': 'Invalid token'})
        response.status_code = 401
        return response


def get_token():
    return decode_auth_token(request.headers.get("Authorization"))
