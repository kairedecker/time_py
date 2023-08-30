import sqlite3
from models import Workday, DbReturn, EnumDbReturn

def create_connection(db_file):

    con = None
    try: 
        con = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        return con

def create_manual_time_entry(con, workday: Workday):
    data_tuple = workday.db_str()
    statement = '''
    SELECT * FROM times WHERE date = ? 
    '''
    date = data_tuple[0]
    try:
        c = con.cursor()
        c.execute(statement, (date,))
        data = c.fetchone()
        if data:
            record_workday = Workday()
            record_workday.set_time_from_db(date= data[0],start_time=data[1], end_time=data[2], pause=data[3], day_type=data[4], fiori_entry=data[5])
            return DbReturn(EnumDbReturn.RECORD_AVAILABLE, data=record_workday)
    except sqlite3.Error as e:
        print(e)
        return DbReturn(EnumDbReturn.ERROR)
    
    statement = '''
    INSERT INTO times
    (date, start_time, end_time, pause, day_type, fiori_entry)
    VALUES(?,?,?,?,?,?)
    '''
    
    try:
        c = con.cursor()
        c.execute(statement, data_tuple)
        con.commit()
        return DbReturn(EnumDbReturn.DONE)
    except sqlite3.Error as e:
        print(e)
        return DbReturn(EnumDbReturn.ERROR)

def all_entries(con):
    statement='''
    SELECT * FROM times
    '''
    try: 
        c = con.cursor()
        c.execute(statement)
        data = c.fetchall()
        
        workdays = []
        for day in data:
            workday = Workday()
            workday.set_time_from_db(day[0], day[1], day[2], day[3], day[4], day[5])
            workdays.append(workday)
        return DbReturn(EnumDbReturn.DONE, data=workdays)
    except sqlite3.Error as e:
        print(e)
        return DbReturn(EnumDbReturn.ERROR)

def create_time_table(con):
    statement = '''
    CREATE TABLE IF NOT EXISTS times (
        date text,
        start_time text,
        end_time text,
        pause text,
        day_type text,
        fiori_entry text
    );
    '''
    try:
        c = con.cursor()
        c.execute(statement)
        return DbReturn(EnumDbReturn.DONE)
    except sqlite3.Error as e:
        print(e)
        return DbReturn(EnumDbReturn.ERROR)


