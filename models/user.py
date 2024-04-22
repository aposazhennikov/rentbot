import psycopg2
from datetime import datetime
from config import *


class User:
    def __init__(self):
        # loading from config
        try:
            self.conn = psycopg2.connect(host=DB_HOST,
                                         dbname=DB_NAME,
                                         user=DB_USER,
                                         password=DB_PASSWORD)
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            # Need to add meaningful exception
            return None

    # Получаем любой(ые) элемент(ы) из таблицы users
    # IMPORT FROM OLD CODE AND MODIFED
    def get_user_args(self, chat_id, *args):
        '''
        Need to add description of function
        And change HARDCODE "api.users" and "chat_id" to values which getting from input FUNC
        '''
        data = dict()

        with self.conn:
            for key in args:
                try:
                    self.cursor.execute(f"SELECT {key} FROM api.users WHERE id = %s", (chat_id,))
                    result = self.cursor.fetchall()
                    for row in result:
                        data[key] = str(row[0])
                except psycopg2.Error as e:
                    return None
            return data

    def get_by_id(self, chat_id):
        '''
        Need to add description of function
        Again no HARDCODE PLS
        '''
        print(f'get user {chat_id}')

        try:
            with self.conn as conn:
                with self.cursor as cur:
                    cur.execute(
                        "SELECT * FROM api.users WHERE id=%s", (chat_id,))
                    result = cur.fetchone()

            if result and len(result) == 10:
                # PLS NO HARDCODE
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
            return None

    def create(self, params):
         '''
        Need to add description of function
        '''
        print('add user')

    def update(self, params):
        '''
        Need to add description of function
        '''
        print('update user')

    def delete(self, chat_id):
        '''
        Need to add description of function
        '''
        print('delete user')

    def get_all(self):
        '''
        Need to add description of function
        '''
        print('get all user')
