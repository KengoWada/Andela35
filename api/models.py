from db import DatabaseConnection
import re

db = DatabaseConnection()

class Users:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def validate_input(self):
        if not self.username or self.username.isspace():
            return 'Username field can not be left empty.'
        elif not self.email or self.email.isspace():
            return 'Email field can not be left empty.'
        elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", self.email):
            return 'Enter a valid email address.'
        elif not self.password or self.password.isspace():
            return 'Password field can not be left empty.'
        elif len(self.password) < 8:
            return 'Password has to be longer than 8 characters.'
    
    def check_user_exist(self):
        username = db.check_username(self.username)
        email = db.check_email(self.email)

        if username != None:
            return 'Username is taken.'
        if email != None:
            return 'Email already has an account.'

    @staticmethod
    def login_validate(username, password):
        if not username or username.isspace():
            return 'Username field can not be left empty.'
        elif not password or password.isspace():
            return 'Password field can not be left empty.'
        else:
            return None
