
import datetime
from models import Workday, EnumDayType, EnumDbReturn
from db import *
import re


def get_manual_times_today():
    date = datetime.date.today()
    print("Für folgendes Datum: " + str(date) + " :")
    '''
    start_hour = input('Beginn Stunden: ')
    start_minute = input('Beginn Minute: ')
    end_hour = input('Ende Stunden: ')
    end_minute = input('Ende Minuten: ')
    pause_hour = input('Pause Stunden: ')
    pause_min = input('Pause Minuten: ')
    '''
    
    while True:
        start_time = input('Beginn (Format - XX:XX): ')
        end_time = input('Ende (Format - XX:XX): ')
        pause = input('Pause (Format - XX:XX): ')
        pause_reg = re.search('^(?:([01]?\d|2[0-3]):([0-5]?\d))?$', end_time)
        start_reg = re.search('^(?:([01]?\d|2[0-3]):([0-5]?\d))?$', start_time)
        end_reg = re.search('^(?:([01]?\d|2[0-3]):([0-5]?\d))?$', end_time)
        if pause_reg and start_reg and end_reg:
            break
        else:
            print("Bitte Zeiten nach vorgegebenem Format erfassen!")
    

    workday = Workday()
    try:
        workday.set_time_manual_today(start_time, end_time, pause)
    except Exception as e:
        print(e)

    
    while True:
        print("Folgende Day types sind verfügbar: ")
        for day_type in EnumDayType:
            print(day_type.value)
        day_type = input('Day type angeben: ')
        if day_type in EnumDayType:
            workday.set_day_type(day_type)
            break
        else: 
            print("Day type nicht gefunden!")
    return workday


def main():
    connection = create_connection(r"C:\Users\DEU301998\OneDrive - ABB\Time\time.db")
    if connection != None:
        create_time_table(connection)
        while True:
            print("Bitte wählen: ")
            command = input("Anlegen, Löschen, Anzeigen, Fiori, Beenden: ")
            command = command.lower()
            if command  == "anlegen":
                workday = get_manual_times_today()
                res = create_manual_time_entry(connection, workday)
                if res.return_type == EnumDbReturn.RECORD_AVAILABLE:
                    print("Eintrag schon vorhanden: ")
                    print(res.data)
            elif command == "löschen":
                pass
            elif command == "anzeigen":
                db_return = all_entries(connection)
                for workday in db_return.data:
                    print(workday)
            elif command == "fiori":
                pass
            elif command == "beenden":
                connection.close()
                break
            else:
                print("Bitte eine der verfügbaren Optionen wählen! \n")
        
if __name__ == '__main__':
    main()
