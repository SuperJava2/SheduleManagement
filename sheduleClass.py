from pkg_resources import ZipProvider
from win32gui import PtInRect, Shell_NotifyIcon
from modelShedule import MyShedule,MyClass 
from os import read
from win10toast import ToastNotifier
from datetime import datetime
import webbrowser
import json
import time

def notificador(title,body):
    toaster = ToastNotifier();
    toaster.show_toast(title, body, duration = 20)

def open_browser(url):
    webbrowser.open(url);

def get_date(): 
    return {'day':datetime.today().strftime('%A'),'time':time.strftime('%H:%M:%S', time.localtime())}

def read_json_day(filename):
    date = get_date()
    
    data = json.load(open(filename))
    
    for x in data:
        listClasses = []
        if date['day'] == x['day']:
            for y in data[0]['classes']:
                if y['startHour'] >= date['time']:
                    listClasses.append(MyClass(y['name'], y['url'],y['startHour'], y['endHour']))
                    
            return MyShedule(x['day'], listClasses)
    
def time_to_sec(time_str):
    return sum(x * int(t) for x, t in zip([1, 60], reversed(time_str.split(":"))))            


def main():
    shedule = read_json_day('shedule.json')
    
    # while get_date()['time'] != shedule.myclass[0].start: 
    for x in shedule.myclass:
        tiempoActual = time_to_sec(get_date()['time'])
        time.sleep(2)
        tiempoClase = time_to_sec(shedule.myclass[0].start)
        
        # print(shedule.myclass[0].url)
        # print(tiempoClase-tiempoActual)
        print('Esperando....')
        aux = tiempoClase-tiempoActual
        if aux > 0 :
            time.sleep(aux)
            open_browser(shedule.myclass[0].url)
            notificador(shedule.myclass[0].name, shedule.myclass[0].url)
            # shedule.myclass.pop()
            shedule = read_json_day('shedule.json')
        else:
            print('Tiempo inválido.')
        # shedule.myclass.pop()
        # print("LA MERA VERGA")
    # print(time_to_sec(get_date()['time']))
    # print(get_date()['time'])
    # format = '%H:%M'
    # time = (datetime.strptime(get_date()['time'], format)) - (datetime.strptime(shedule.myclass[0].start, format))
    # print(time)
    # print( shedule.myclass[0].startHour)

    # if get_date()['time'] == shedule.myclass[0].startHour:
    
        
if __name__ == "__main__":
    main()

