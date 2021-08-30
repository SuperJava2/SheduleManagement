# -=- encoding: utf-8 -=-
#
# Copyright (C) 2021 Luis Ángel Glez Gtz.

from modelShedule import MyShedule,MyClass 
from win10toast import ToastNotifier
from datetime import datetime, timedelta
import webbrowser
import json
import time
import re

def notificador(title,body):
    toaster = ToastNotifier();
    toaster.show_toast(title, body, duration = 10, icon_path='assets/icono.ico')

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
    return  timedelta(**dict(zip("hours minutes seconds".split(), map(int, re.findall('\d+', time_str))))).total_seconds()


def main():
    
    shedule = read_json_day('lib/shedule.json')
    
    for x in shedule.myclass:
        tiempoActual = time_to_sec(get_date()['time'])
        tiempoClase = time_to_sec(x.start)

        aux = tiempoClase-tiempoActual
        # print('Esperando: ' + aux + " segundos")
        print(aux)
        
        if aux > 0 :
            time.sleep(aux)
            open_browser(x.url)
            notificador(x.name, x.url)
            # shedule = read_json_day('shedule.json')
        else:
            print('Tiempo inválido.')
        
if __name__ == "__main__":
    main()

