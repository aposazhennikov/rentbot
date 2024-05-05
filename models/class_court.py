from datetime import timedelta
from datetime import datetime
from titles import title

# set max calendar size and get chat_id for titles


class Calendar:
    def __init__(self, chat_id):
        self.max_next = 9
        self.time_start = 8
        self.time_finish = 23
        self.max_slots = 4
        self.time_range = self.time_finish - self.time_start
        self.chat_id = chat_id

    # we get the weekdays and their short names when we look at the court
    async def get_days(self):
        days = []
        start_day = datetime.now()
        short_weekdays = await self.get_short_weekday()

        for i in range(self.max_next):
            day = start_day + timedelta(days=i)
            short_day = short_weekdays[int(day.weekday())]
            title_day = f'{day.strftime("%d.%m.%Y")} ({short_day})'

            if start_day == datetime.now():
                title_day += '*'

            days.append(title_day)

        return days

    # here is we just load title for weekdays
    async def get_short_weekday(self):
        weekdays = dict()
        for i in range(7):
            weekdays[i] = await title.load_title(
                self.chat_id, f'title_weekday_short_{i}')
        return weekdays

    async def get_time(self):
        time = []
        for i in range(self.time_range):
            i += self.time_start
            for j in range(2):
                j *= 30
                if j == 0:
                    j = '00'
                time.append(f'{i}:{j}')
        return time
