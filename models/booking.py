import psycopg2
from config import *
from datetime import datetime
from datetime import timedelta


class Booking:
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
            self.table = 'booking'
        except psycopg2.Error as e:
            print(e)
            # Need to add meaningful exception
            return None

    async def create(self, params):
        print('booked')
        params["is_active"] = 1
        params["created_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        columns = ', '.join(params.keys())
        placeholders = ', '.join(['%s'] * len(params))

        # Проверка на пересечение временных интервалов
        check_query = f"SELECT COUNT(*) FROM {self.scheme}.{self.table} WHERE date = %s AND court_id = %s AND (%s, %s) OVERLAPS (start_time, end_time)"
        overlap_params = (params['date'], params['court_id'],
                          params['start_time'], params['end_time'])

        try:
            with self.conn:
                self.cursor.execute(check_query, overlap_params)
                overlap_count = self.cursor.fetchone()[0]

                if overlap_count > 0:
                    print("Временной интервал пересекается с другим пользователем.")
                    return False

                insert_query = f"INSERT INTO {self.scheme}.{self.table} ({columns}) VALUES ({placeholders})"
                self.cursor.execute(insert_query, list(params.values()))
            return True
        except psycopg2.Error as e:
            print(e)
            return False

    async def get_times_by_datetime(self, date, court_id, time_start=None):
        date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

        try:
            with self.conn:
                if time_start:
                    time_start = datetime.strptime(
                        f'{date} {time_start}', "%Y-%m-%d %H:%M").strftime("%Y-%m-%dT%H:%M:%S.%f")
                    print(f'try get time for time: {time_start}')
                    query = f"SELECT start_time, end_time, user_id FROM {self.scheme}.{self.table} WHERE date = %s AND court_id = %s AND (start_time > %s OR start_time = %s)"
                    self.cursor.execute(
                        query, (date, court_id, time_start, time_start))
                else:
                    query = f"SELECT start_time, end_time, user_id FROM {self.scheme}.{self.table} WHERE date = %s AND court_id = %s"
                    self.cursor.execute(query, (date, court_id))
                times = self.cursor.fetchall()
                return times
        except psycopg2.Error as e:
            print(e)
            return False

    async def get_user_by_datetime(self, date, court_id, time_start):
        date = datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
        time_start = datetime.strptime(
            f'{date} {time_start}', "%Y-%m-%d %H:%M").strftime("%Y-%m-%dT%H:%M:%S.%f")
        query = f"SELECT u.user_name, u.first_name, b.user_id, b.start_time, b.end_time, b.id, b.date, b.court_id FROM {self.scheme}.{self.table} as b LEFT JOIN {self.scheme}.users as u ON u.id = b.user_id WHERE b.date = %s AND b.court_id = %s AND %s BETWEEN b.start_time AND b.end_time ORDER BY b.start_time DESC LIMIT 1"

        try:
            with self.conn:
                self.cursor.execute(query, (date, court_id, time_start))
                result = self.cursor.fetchone()

                if result and len(result) == 8:
                    return {
                        "user_name": result[0],
                        "first_name": result[1],
                        "user_id": result[2],
                        "start_time": result[3],
                        "end_time": result[4],
                        "id": result[5],
                        "date": result[6],
                        "court_id": result[7]
                    }
                else:
                    return None
        except psycopg2.Error as e:
            print(e)
            return False

    async def get(self, book_id):
        query = f"SELECT u.user_name, u.first_name, b.user_id, b.start_time, b.end_time, b.id, b.date, b.court_id FROM {self.scheme}.{self.table} as b LEFT JOIN {self.scheme}.users as u ON u.id = b.user_id WHERE b.id = %s"

        try:
            with self.conn:
                self.cursor.execute(query, (book_id,))
                result = self.cursor.fetchone()

                if result and len(result) == 8:
                    return {
                        "user_name": result[0],
                        "first_name": result[1],
                        "user_id": result[2],
                        "start_time": result[3],
                        "end_time": result[4],
                        "id": result[5],
                        "date": result[6],
                        "court_id": result[7]
                    }
                else:
                    return None
        except psycopg2.Error as e:
            print(e)
            return False

    async def get_fields(self):
        args = [
            "court_id",
            "start_time",
            "end_time",
            "date",
            "additional_member",
            "type",
            "user_id",
            "created_at",
            "is_active"
        ]
        return args

    async def delete(self, book_id):
        print(f'delete booking {book_id}')
        query = f"DELETE FROM {self.scheme}.{self.table} WHERE id = %s AND user_id = %s"
        try:
            with self.conn:
                self.cursor.execute(query, (book_id, self.chat_id))
            return True
        except psycopg2.Error as e:
            print(e)
            return False

    async def get_all(self, date=None):
        if date:
            date_formatted = datetime(datetime.strftime(
                date, '%d.%m.%Y')).strftime("%Y-%m-%d")
            query = f"SELECT u.user_name, u.first_name, b.user_id, b.start_time, b.end_time, b.id, b.date, b.court_id FROM {self.scheme}.{self.table} as b LEFT JOIN {self.scheme}.users as u ON u.id = b.user_id WHERE b.user_id = %s AND b.date = %s ORDER BY court_id, date, start_time ASC"
        else:
            date_formatted = (
                datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            query = f"SELECT u.user_name, u.first_name, b.user_id, b.start_time, b.end_time, b.id, b.date, b.court_id FROM {self.scheme}.{self.table} as b LEFT JOIN {self.scheme}.users as u ON u.id = b.user_id WHERE b.user_id = %s AND b.date > %s ORDER BY court_id, date, start_time ASC"

        try:
            with self.conn:
                self.cursor.execute(query, (self.chat_id, date_formatted))
                results = self.cursor.fetchall()

                if results:
                    rows = []

                    for result in results:
                        row = {
                            "user_name": result[0],
                            "first_name": result[1],
                            "user_id": result[2],
                            "start_time": result[3],
                            "end_time": result[4],
                            "id": result[5],
                            "date": result[6],
                            "court_id": result[7]
                        }
                        rows.append(row)
                    return rows
                else:
                    return None
        except psycopg2.Error as e:
            print(e)
            return False

    async def nearest_sunday(self):
        today = datetime.now().date()
        days_until_sunday = (6 - today.weekday()) % 7
        nearest_sunday_date = today + timedelta(days=days_until_sunday)
        return nearest_sunday_date

    async def nearest_monday(self):
        today = datetime.now().date()
        days_since_monday = today.weekday()
        nearest_monday_date = today - \
            timedelta(days=days_since_monday)
        return nearest_monday_date

    async def calculate_intervals_count(self):
        monday = await self.nearest_monday()
        sunday = await self.nearest_sunday()
        print(f'{monday} {sunday}')

        query = f"SELECT b.start_time, b.end_time FROM {self.scheme}.{self.table} as b WHERE b.user_id = %s AND b.date> %s AND b.date<%s"

        try:
            with self.conn:
                self.cursor.execute(query, (self.chat_id, monday, sunday))
                results = self.cursor.fetchall()

                if results:
                    rows = []

                    for result in results:
                        row = {
                            "start_time": result[0],
                            "end_time": result[1]
                        }
                        rows.append(row)
                    intervals = await self.count_intervals(rows)

                    return intervals
                else:
                    return 0
        except psycopg2.Error as e:
            print(e)
            return False

    async def count_intervals(self, rows):
        # Создаем список для хранения всех промежутков времени
        all_intervals = []
        slots_weekday = []
        slots_primetime = []

        # Проходимся по каждой записи в rows
        for row in rows:
            start_time = row['start_time']
            end_time = row['end_time']

            # Добавляем все промежутки времени в список all_intervals
            current_time = start_time

            while current_time < end_time:
                all_intervals.append(
                    (current_time, min(end_time, current_time + timedelta(minutes=30))))
                current_time += timedelta(minutes=30)

                # Заполняем соответствующие слоты
                if start_time.hour < 17:
                    slots_weekday.append((start_time, end_time))
                else:
                    slots_primetime.append((start_time, end_time))
                # Подсчитываем количество бронирований в субботу и воскресенье
                if start_time.weekday() in [5, 6]:  # Суббота # Воскресенье
                    slots_primetime.append((start_time, end_time))

        # Возвращаем количество промежутков и слоты
        return {'booking': len(rows), 'slots_all': len(all_intervals), 'slots_weekday': len(slots_weekday), 'slots_primetime': len(slots_primetime)}
