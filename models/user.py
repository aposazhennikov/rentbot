import psycopg2
import logging
from datetime import datetime
from config import *


# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD)
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            logger.error(f"Error connection SQL: {e}")
            raise

    # Получаем любой(ые) элемент(ы) из таблицы users
    def get_user_args(self, chat_id, *args):
        data = dict()
        with self.conn:
            for key in args:
                try:
                    self.cursor.execute(
                        f"SELECT {key} FROM api.users WHERE id = %s", (chat_id,))
                    result = self.cursor.fetchall()
                    for row in result:
                        data[key] = str(row[0])
                except psycopg2.Error as e:
                    logger.error(f"Error executing SQL query:: {e}")
            return data

    def get_by_id(self, chat_id):
        print(f'get user {chat_id}')

        try:
            with self.conn as conn:
                with self.cursor as cur:
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
