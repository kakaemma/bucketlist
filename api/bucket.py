from flask import jsonify, request, json, render_template
from api import create_app
from classes.auth import Authenticate
from classes.bucket import Bucket
from classes.item import Item
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
@validate_content_type
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
        return response

    except KeyError:
        invalid_keys()
#-------------------------------------------------------------------------

@app.route('/auth/login',  methods=['POST'])
@validate_content_type
def login():
    """
    End point for login
    """

    request.get_json(force=True)
    try:
        email = request.json['email']
        password = request.json['password']
        response = Authenticate.login(email, password)
        return response
    except KeyError:
        invalid_keys()
#-------------------------------------------------------------------------

@app.route('/auth/reset-password', methods=['POST'])
@validate_content_type
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
        return response

    except KeyError:
        invalid_keys()
#-------------------------------------------------------------------------


@app.route('/buckets', methods=['POST'])
@validate_content_type
@validate_token
def add_bucket():
    """ 
    End point for adding bucket
    """
    request.get_json(force=True)
    try:
        name = request.json['name']
        desc = request.json['desc']
        response = Bucket.add_bucket(name, desc)
        return response
    except KeyError:
        invalid_keys()

# -------------------------------------------------------------------------

@app.route('/buckets', methods=['GET'])
@validate_token
def get_buckets():
    """ 
        This endpoints gets all buckets
        """
    try:
        response  = Bucket.get_all_buckets()
        return response
    except KeyError:
        invalid_keys()

#-------------------------------------------------------------------------


@app.route('/buckets/<int:bucket_id>', methods=['GET'])
@validate_token
def get_bucket(bucket_id):
    """ 
    This endpoints gets all buckets
    """
    try:
        response = Bucket.get_single_bucket(bucket_id)
        return response
    except KeyError:
        invalid_keys()
#-------------------------------------------------------------------------


@app.route('/buckets/<int:bucket_id>', methods=['PUT'])
@validate_content_type
@validate_token
def modify_bucket(bucket_id):
    """ 
    This endpoints gets all buckets
    """
    request.get_json(force=True)
    try:
        name = request.json['name']
        desc = request.json['desc']
        response = Bucket.modify_bucket(bucket_id, name, desc)
        return response
    except KeyError:
        invalid_keys()
#-------------------------------------------------------------------------


@app.route('/buckets/<int:bucket_id>', methods=['DELETE'])
@validate_token
def delete_bucket(bucket_id):
    """ 
    This endpoints gets all buckets
    """
    try:
        response = Bucket.delete_bucket_from_bucket_list(bucket_id)
        return response
    except KeyError:
        invalid_keys()
#-------------------------------------------------------------------------

@app.route('/buckets/<int:bucket_id>/items', methods=['POST'])
@validate_content_type
@validate_token
def add_item(bucket_id):
    request.get_json(force=True)
    try:
        name = request.json['name']
        status = request.json['status']
        response = Item.add_item(name, status, bucket_id)
        return response
    except KeyError:
        invalid_keys()
#---------------------------------------------------------------------------

@app.route('/buckets/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
@validate_content_type
@validate_token
def edit_item(bucket_id, item_id):
    request.get_json(force=True)
    try:
        name = request.json['name']
        status = request.json['status']
        response = Item.edit_item(bucket_id, name, status, item_id,)
        return response

    except KeyError:
        invalid_keys()

@app.route('/buckets/<int:bucket_id>/items/<int:item_id>', methods=['DELETE'])
@validate_token
def delete_item(bucket_id, item_id):
    try:
        response = Item.delete_item(bucket_id, item_id)
        return response
    except KeyError:
        invalid_keys()

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