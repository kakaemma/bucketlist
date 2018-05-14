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

@app.route('/auth/login', methods=['POST'])
def login():
    request.get_json(force=True)
    try:
        email = request.json['email']
        password = request.json['password']
        response = Authenticate.login(email, password)
        print(response)
        response = operation_successful(response)
        return  response
    except KeyError:
        invalid_keys()





def invalid_keys():
    response = jsonify({'Error': 'Invalid keys'})
    response.status_code = 400
    return  response

def operation_successful(response):
    if response.status_code == 200 and \
            response.data.decode()=='Successfully logged in':
        data = json.loads(response.data.decode())
        response = jsonify(data)
        response.status_code =200
    return response



