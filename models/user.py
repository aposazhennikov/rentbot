import psycopg2

from datetime import datetime
from config import *


class User:
    def __init__(self):
        self.db_host = DB_HOST
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD

    def get_by_id(self, chat_id):
        print(f'get user {chat_id}')

        try:
            with psycopg2.connect(
                host=self.db_host,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM api.users WHERE id=%s", (chat_id,))
                    result = cur.fetchone()

            if result and len(result) == 10:
                return {
                    "id": result[0],
                    "birth_day": result[1],
                    "ntrp": result[2],
                    "first_name": result[3],
                    "last_name": result[4],
                    "tennis_experience": result[5],
                    "phone_number": result[6],
                    "user_name": result[7],
                    "description": result[8],
                    "created_at": result[9],
                }
            else:
                return None
        except psycopg2.Error as e:
            print(f"Error executing SQL query: {e}")
            return None

    def create(self, params):
        print('add user')

    def update(self, params):
        print('update user')

    def delete(self, chat_id):
        print('delete user')

    def get_all(self):
        print('get all user')
