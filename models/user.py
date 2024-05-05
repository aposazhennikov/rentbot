import psycopg2
from config import *
import time


class User:
    def __init__(self, chat_id=None):
        # loading from config
        try:
            self.conn = psycopg2.connect(host=DB_HOST,
                                         dbname=DB_NAME,
                                         user=DB_USER,
                                         password=DB_PASSWORD)
            self.cursor = self.conn.cursor()
            self.scheme = DB_USER_SCHEME
            self.chat_id = chat_id
        except psycopg2.Error as e:
            # Need to add meaningful exception
            return None

    # Получаем любой(ые) элемент(ы) из таблицы users
    # IMPORT FROM OLD CODE AND MODIFED
    async def get_user_args(self, *args):
        data = dict()

        with self.conn:
            for key in args:
                try:
                    self.cursor.execute(
                        f"SELECT {key} FROM {self.scheme}.users WHERE id = %s", (self.chat_id,))
                    result = self.cursor.fetchall()
                    for row in result:
                        data[key] = str(row[0])
                except psycopg2.Error as e:
                    return None
            return data

    async def get(self):
        '''
        Need to add description of function
        Again no HARDCODE PLS
        '''
        print(f'get user {self.chat_id}')

        try:
            with self.conn as conn:
                with self.cursor as cur:
                    cur.execute(
                        f"""SELECT id, birth_day, ntrp, first_name, last_name, 
                        tennis_experience, phone_number, user_name, description, 
                        created_at, gender, id_status FROM {self.scheme}.users WHERE id=%s""", (self.chat_id,))
                    result = cur.fetchone()

            if result and len(result) == 12:
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
                    "gender": result[10],
                    "id_status": result[11],
                }
            else:
                return None
        except psycopg2.Error as e:
            return None

    async def get_fields_profile(self):
        args = [
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "birth_day",
            "ntrp",
            "tennis_experience",
            "description"
        ]
        return args

    async def update(self, params):
        '''
        this function update user in database
        '''
        print('update user')
        update_query = f"UPDATE {self.scheme}.users SET"
        values = []

        for key, value in params.items():
            update_query += f" {key} = %s,"
            values.append(value)

        update_query = update_query.rstrip(',') + " WHERE id = %s"
        values.append(self.chat_id)

        try:
            with self.conn:
                self.cursor.execute(update_query, values)
            return True
        except psycopg2.Error as e:
            return False

    async def delete(self):
        '''
        this function delete user from database
        '''
        print('delete user')
        try:
            with self.conn:
                self.cursor.execute(
                    f"DELETE FROM {self.scheme}.users WHERE id = %s", (self.chat_id,))
            return True
        except psycopg2.Error as e:
            return False

    # this function remove user from vision
    async def remove(self):
        print('remove user')
        try:
            with self.conn:
                self.cursor.execute(
                    f"UPDATE {self.scheme}.users SET status=1 WHERE id = %s", (self.chat_id,))
            return True
        except psycopg2.Error as e:
            return False

    async def create(self, params):
        '''
        this function create new user in database
        '''
        print('add user')
        params["created_at"] = int(time.time())
        columns = ', '.join(params.keys())
        placeholders = ', '.join(['%s'] * len(params))
        insert_query = f"INSERT INTO {self.scheme}.users ({columns}) VALUES ({placeholders})"

        try:
            with self.conn:
                self.cursor.execute(insert_query, list(params.values()))
            return True
        except psycopg2.Error as e:
            return False

    def get_all(self):
        '''
        Need to add description of function
        '''
        print('get all user')
