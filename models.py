import enum
import datetime
import re

class MyEnumMeta(enum.EnumMeta): 
    def __contains__(cls, item): 
        return isinstance(item, cls) or item in [v.value for v in cls.__members__.values()] 

class EnumDayType(enum.Enum, metaclass=MyEnumMeta):
    OFFICE = 'office'
    HOMEOFFICE = 'home'
    GLAZ = 'GLAZ'
    URLAUB = 'urlaub'
    REISE = 'reise'
    OPEN = ''

class EnumDbReturn(enum.Enum):
    DONE = 0
    ERROR = 1
    RECORD_AVAILABLE = 2

class DbReturn():
    def __init__(self, return_type: EnumDbReturn, data={}):
        self.return_type = return_type
        self.data = data
    
    def get_return_type(self):
        return self.return_type
    
    def get_data(self):
        return self.data

class Workday(): 
    def __init__(self, date = 0, start_time = 0, end_time = 0, pause = 0, day_type = EnumDayType.HOMEOFFICE, fiori_entry='no') -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.pause = pause
        self.date = date
        self.day_type = day_type
        self.fiori_entry = fiori_entry

    def set_time_manual_today(self, start_time, end_time, pause):
        pause_reg = re.search('^(?:([01]?\d|2[0-3]):([0-5]?\d))?$', end_time)
        start_reg = re.search('^(?:([01]?\d|2[0-3]):([0-5]?\d))?$', start_time)
        end_reg = re.search('^(?:([01]?\d|2[0-3]):([0-5]?\d))?$', end_time)
        if not pause_reg:
            raise Exception('Pause time format not correct: XX:XX')
        if not start_reg:
            raise Exception('Start time format not correct: XX:XX ')
        if not end_reg:
            raise Exception('End time format not correct: XX:XX ')
        self.date = datetime.date.today()
        self.start_time = datetime.datetime.strptime(start_time, "%H:%M")
        self.end_time = datetime.datetime.strptime(end_time, "%H:%M")
        pause = pause.split(':')
        self.pause = datetime.timedelta(minutes=int(pause[1]), hours=int(pause[0]))
        
    def set_time_from_db(self, date, start_time, end_time, pause, day_type, fiori_entry) -> None:
        self.date = date
        self.start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")
        self.end_time = datetime.datetime.strptime(end_time, "%H:%M:%S")
        pause = pause.split(':')
        self.pause = datetime.timedelta(minutes=int(pause[1]), hours=int(pause[0]))
        self.day_type = day_type
        self.fiori_entry = fiori_entry

    def db_str(self):
        workday_tuple = (str(self.date), str(self.start_time.time()), str(self.end_time.time()), str(self.pause), str(self.day_type), self.fiori_entry)
        return workday_tuple

    def get_differ_start_end(self):
        return self.end_time - self.start_time
    
    def get_differ_with_pause(self):
        return self.get_differ_start_end() - self.pause
    
    def set_day_type(self, day_type: EnumDayType):
        self.day_type = day_type


    def __str__(self) -> str:
        return str({
            "Date": str(self.date),
            "Fiori Eintrag": self.fiori_entry,
            'Arbeitszeit mit Pause': str(self.get_differ_with_pause()),
            'Arbeitszeit ohne Pause': str(self.get_differ_start_end()),
            "Start Time": str(self.start_time.time()),
            "End Time": str(self.end_time.time()),
            "Pause": str(self.pause),
            "Day Type": self.day_type,
        })