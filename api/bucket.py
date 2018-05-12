from flask import jsonify, request, json, render_template
from api import create_app

app = create_app('TestingEnv')


@app.route('/')
def index():
    """ Index route """
    return render_template('index.html')


@app.route('/auth/register')
def register():
    """ """
    return ''


@app.route('/auth/login')
def login():
    pass




