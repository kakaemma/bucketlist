from flask import jsonify, request, json, render_template
from api import create_app
from classes.auth import Authenticate
from classes.bucket import Bucket
from utility.utility import validate_content_type, validate_token


app = create_app('TestingEnv')


@app.route('/')
def index():
    """ 
    Index route 
    """
    return render_template('index.html')
#-------------------------------------------------------------------------

@app.route('/auth/register', methods=['POST'])
def register():
    """ 
    Register a user with this endpoint 
    """

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
#-------------------------------------------------------------------------

@app.route('/auth/login', methods=['POST'])
def login():
    """
    End point for login
    """

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
#-------------------------------------------------------------------------

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """
    End point for reset password
    """

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
#-------------------------------------------------------------------------


@app.route('/buckets', methods=['POST'])
def add_bucket():
    """ 
    End point for adding bucket
    """
    try:
        name = request.json['name']
        desc = request.json['desc']
        response = Bucket.add_bucket(name, desc)
        response = operation_successful(response)
        return response
    except KeyError:
        invalid_keys()

#-------------------------------------------------------------------------

@app.route('/buckets', methods=['GET'])
def get_buckets():
    """ 
    This endpoints gets all buckets
    """
    try:
        pass
    except KeyError:
        invalid_keys()
#-------------------------------------------------------------------------

@app.route('/auth/logout', methods=['POST'])
def logout():
    pass
#-------------------------------------------------------------------------

def invalid_keys():
    """
    Handles invalid keys
    :return: 
    """
    response = jsonify({'Error': 'Invalid keys'})
    response.status_code = 400
    return response
#--------------------------------------------------------------------------

def operation_successful(response):
    """
    Handles successful execution of operations
    :param response: 
    :return: 
    """
    if response.status_code == 201:
        data = json.loads(response.data.decode())
        response = jsonify(data)
        response.status_code = 201
        return response
    return response
#--------------------------------------------------------------------------


def invalid_token():
    """
    Handles invalid tokens
    :return: String
    """
    response = jsonify({'Error': 'Invalid Token '})
    response.status_code = 400
    return response
