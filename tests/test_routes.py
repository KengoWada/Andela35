import unittest
from api.routes import app
import json
from db import DatabaseConnection


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()
        self.db = DatabaseConnection()

    def test_user_register(self):
        user = {
            'username': 'KengoWada',
            'email': 'kengowada@nasa.com',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'KengoWada successfully registered.')
    
    def test_register_username_twice(self):
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user2 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        response2  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user2)
        )

        message = json.loads(response2.data.decode())

        self.assertEqual(message['message'], 'Username is taken.')

    def test_register_email_twice(self):
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user2 = {
            'username': 'WadaKengo',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        response2  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user2)
        )

        message = json.loads(response2.data.decode())

        self.assertEqual(message['message'], 'Email already has an account.')

    def test_register_empty_username(self):
        user = {
            'username': '',
            'email': 'kengowada@nasa.com',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Username field can not be left empty.')

    def test_register_empty_email(self):
        user = {
            'username': 'kengowada',
            'email': '',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Email field can not be left empty.')

    def test_register_empty_password(self):
        user = {
            'username': 'kengowada',
            'email': 'kengowada@nasa.com',
            'password': ''
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Password field can not be left empty.')

    def test_register_invalid_email(self):
        user = {
            'username': 'kengowada',
            'email': 'kengonasa.com',
            'password': 'kengowada'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Enter a valid email address.')

    def test_register_password_length(self):
        user = {
            'username': 'kengowada',
            'email': 'kengowada@nasa.com',
            'password': 'keda'
        }

        response  = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Password has to be longer than 8 characters.')

    def test_user_login(self):
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'KengoWada',
            'password': 'kengowada'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'KengoWada successfully logged in.')

    def test_user_login_empty_username(self):
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': '',
            'password': 'kengowada'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Username field can not be left empty.')

    def test_user_login_empty_password(self):
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'KengoWada',
            'password': ''
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Password field can not be left empty.')
    
    def test_login_wrong_username(self):
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'Kengo Wada',
            'password': 'kengowada'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Wrong login credentials.')

    def test_login_wrong_password(self):
        user1 = {
            'username': 'KengoWada',
            'email': 'kengowada@apple.com',
            'password': 'kengowada'
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'KengoWada',
            'password': 'kengowada1234'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'Wrong login credentials.')

    def tearDown(self):
        self.db.drop_table('users')
    