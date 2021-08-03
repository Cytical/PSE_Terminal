import requests
import json
import calendar
from timeit import default_timer as timer
from datetime import datetime


def isweekday(date):
    month = int(date[0])
    day = int(date[1])
    year = int(date[2])
    if calendar.weekday(year,month,day) == 5:
        date[1] = str(int(date[1]) - 1)
    elif calendar.weekday(year,month,day) == 6:
        date[1] = str(int(date[1]) - 2)
    if len(date[0]) < 2:
            date[0] = "0" + date[0]
    if len(date[1]) < 2:
        date[1] = "0" + date[1]
    date = date[2]+date[0]+date[1]
    return date


symbol = 'ACEN'
date = [datetime.today().strftime('%m'), str(int(datetime.today().strftime('%d'))-1), datetime.today().strftime('%Y')]
current = isweekday(date)

start = timer()
date = current[0:4] + "-"+ current[4:6] + "-" + current[6:8]
r = requests.get("http://phisix-api.appspot.com/stocks/" + symbol + ".json")
stock = json.loads(r.text)

a = stock["stock"][0]["percent_change"]
print(a)


end = timer()
time = end - start

print(time)