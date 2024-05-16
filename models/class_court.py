from datetime import timedelta
from datetime import datetime
from titles import title


class Calendar:

    def __init__(self, chat_id):
        # ==== SLOTS ====
        # after 5p.m. for example or weekends (only 1.5 hours)
        self.max_slots_primetime = 3

        # normal_slots_per_day (only 2 hours)
        self.max_slots_per_day = 4

        # ==== DAYS ====
        # how many days we will show for booking
        max_dc = {0: 7, 1: 9, 2: 12}
        self.max_days_calendar = max_dc

        # ==== BOOKING PER WEEK ====
        # how many bookings user can take per week
        max_bw = {0: 2, 1: 3, 2: 5}
        self.max_booking_week = max_bw

        # ==== DESIGN SETTINGS =====
        # max number of time slots in a line
        self.max_row_time = 4
        # max number of date slots per line
        self.max_row_date = 3

        # ====== OLD STANDART SETTING BOOKING =======
        # number of days for booking
        self.max_next_days = 7

        # number of slots a user can occupy at a time
        self.max_slots = 4
        # earliest hour available for booking
        self.time_start = 8
        # latest hour available for booking
        self.time_finish = 23
        # chat_id of user
        self.chat_id = chat_id

    # the function gets the days of the week and their short names in dates
    async def get_days(self, max_days):
        days = []
        start_day = datetime.now()
        short_weekdays = await self.get_short_weekday()

        for i in range(max_days):
            day = start_day + timedelta(days=i)
            short_day = short_weekdays[int(day.weekday())]
            title_day = f'{day.strftime("%d.%m.%Y")} ({short_day})'

            days.append(title_day)

        return days

    # clear dates
    async def get_days_clear(self):
        days = []
        start_day = datetime.now()

        for i in range(self.max_next_days):
            day = start_day + timedelta(days=i)
            title_day = f'{day.strftime("%d.%m.%Y")}'
            days.append(title_day)

        return days

    # here is we just load title for weekdays
    async def get_short_weekday(self):
        weekdays = dict()
        for i in range(7):
            weekdays[i] = await title.load_title(
                self.chat_id, f'title_weekday_short_{i}')
        return weekdays

    # slots for start time of the booking
    async def get_time_start(self):
        time = []

        for i in range(self.time_finish - self.time_start):
            i += self.time_start

            for j in range(2):
                j *= 30
                if j == 0:
                    j = '00'
                time.append(f'{i}:{j}')
        return time

    # slots for end time of the booking
    async def get_time_end(self):
        time = []

        for i in range(self.time_start, self.time_finish + 1):
            for j in range(2):
                if i == self.time_finish and j == 1:
                    break
                j *= 30
                if j == 0:
                    j = '00'
                time.append(f'{i}:{j}')
        return time
