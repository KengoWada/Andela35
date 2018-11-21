import psycopg2
import psycopg2.extras
from pprint import pprint
import os


class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname='learn_db', user='postgres', host='localhost', password='kengo1234', port=5432
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            print('Connected to the database successfully.')

            create_users_table = "CREATE TABLE IF NOT EXISTS users (userId SERIAL NOT NULL PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);"

            self.cursor.execute(create_users_table)
        except:
            pprint('Failed to connect to the database.')

    def register_user(self, username, email, password):
        reg_user = f"INSERT INTO users(username, email, password) VALUES('{username}', '{email}', '{password}');"
        pprint(reg_user)
        self.cursor.execute(reg_user)
    
    def check_username(self, username):
        query = f"SELECT * FROM users WHERE username='{username}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user
    
    def check_email(self, email):
        query = f"SELECT * FROM users WHERE email='{email}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def login(self, username):
        query = f"SELECT * FROM users WHERE username='{username}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        pprint(user)
        return user

    def drop_table(self, table_name):
        drop = f"DROP TABLE {table_name};"
        self.cursor.execute(drop)


if __name__ == '__main__':
    db = DatabaseConnection()
