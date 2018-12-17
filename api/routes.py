from flask import Flask, jsonify, request
import json
from api.models import Users
from db import DatabaseConnection
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'KenG0W@Da4!'


db = DatabaseConnection()

@app.route('/api/v1/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = Users(username, email, password)
    error = user.validate_input()
    exists = user.check_user_exist()

    if error != None:
        return jsonify({'Error': error}), 400
    if not exists:
        password_hash = generate_password_hash(password, method='sha256')
        db.register_user(username, email, password_hash)
        token = create_access_token(username)
        return jsonify({
            'access_token': token,
            'message': f'{username} successfully registered.'
            }), 201
    else:
        return jsonify({'message': exists}), 401     


@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    error = Users.login_validate(username, password)

    if error != None:
        return jsonify({'Error': error}), 400

    user = db.login(username)
    if user == None:
        return jsonify ({'message': 'Wrong login credentials.'}), 400

    if check_password_hash(user['password'], password) and user['username'] == username:
        token = create_access_token(username)
        return jsonify ({
            'access_token': token,
            'message': f'{username} successfully logged in.'
        }), 200
    else:
        return jsonify ({'message': 'Wrong login credentials.'}), 400
        


@app.route('/api/v1/welcome')
@jwt_required
def welcome():
    username = get_jwt_identity()

    return jsonify ({
        'message': f'{username}, Thank you for using Kengo\'s API.'
    }), 200


@app.errorhandler(404)
def page_not_found(e):
    valid_urls = {
        'Signup': {'url': '/api/v1/signup', 'method(s)': 'POST', 'body': {'username': 'String', 'email': 'example@email.com', 'password': 'At least 8 characters.'}},
        'Login': {'url': '/api/v1/login', 'method(s)': 'POST', 'body': {'username': 'String', 'password': 'Enter user password.'}},
        'Welcome': {'url': '/api/v1/welcome', 'method(s)': 'GET', 'header': 'JWT access token.'}
    }
    return jsonify ({
        'Issue': 'You have entered an unknown URL.',
        'Valid URLs': valid_urls,
        'message': 'Please contact Kengo Wada for more details on this API.'
        })