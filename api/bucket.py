from flask import jsonify, request, json, render_template
from api import create_app
from classes.auth import Authenticate

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

@app.route('/auth/login')
def login():
    pass


def invalid_keys():
    response = jsonify({'Error': 'Invalid keys'})
    response.status_code = 400
    return  response

def operation_successful(response):
    if response.status_code == 201:
        data = json.loads(response.data.decode())
        response = jsonify(data)
        response.status_code =201
    return response



