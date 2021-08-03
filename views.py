from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import calendar
from timeit import default_timer as timer
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from home.stocklist import *

# Create your views here.
def index(request):

    r = requests.get(f'https://www.marketwatch.com/investing/stock/psei?countrycode=ph&mod=over_search').text
    soup = BeautifulSoup(r, 'lxml')

    container = soup.find('div', class_ = 'group group--elements left')
    profile = container.find('ul', class_ ='list list--kv list--col50')
    spans = profile.find_all('span', class_ = 'primary')

    company_profile = [span.get_text() for span in spans]
    open = company_profile[0]
    dayrange = company_profile[1].split(" - ")
    low = dayrange[0]
    high = dayrange[1]
    container = soup.find('div', class_ = 'element element--intraday')
    timestamp = container.find('div', class_ = 'intraday__timestamp').text
    container = soup.find('div', class_ = 'element element--intraday')
    try:
        price = container.find('span', class_ = 'value').text
    except: 
        price = container.find('bg-quote', class_ ='value').text
    change = container.find('span', class_ = 'change--point--q').text
    pctchange = container.find('span', class_ = 'change--percent--q').text

    pseindex1 = dict(list(pseindex.items())[:15])
    pseindex2 = dict(list(pseindex.items())[15:30])

    return render(request, 'home/index.html', 
                {'symbol': 'PSEi', 'name': 'Philippine Stock Exchange Index', 'date': timestamp, 
                'open': open, 'close': price, 'low': low, 'high': high, 'pseindex1' : pseindex1,
                'pseindex2': pseindex2, 'stockdict': stockdict, 'pctchange' : pctchange, 'change' : change })

def stock(request, name):
    
    start = timer()
    symbol = name.upper()

    if symbol in stockdict:
        for key, value in stockdict.items():
            if symbol == key:
                company_name = value;
                now = datetime.now()
                time = int(now.strftime("%H").strip('0'))

                #Market Closes at 1pm, thus data is now available
                month = int(datetime.today().strftime('%m'))
                day = int(datetime.today().strftime('%d'))
                year = int(datetime.today().strftime('%Y'))
                print("\n\n\n\n")
                if time > 12 and calendar.weekday(year,month,day) < 5:
                    date = [month,day,year]
                else:
                    date = [month,day -1,year]
                current = isweekday(date)
                stockdate = current[0:4] + "-"+ current[4:6] + "-" + current[6:8]
                print('\n\n\n')
                print(stockdate)
                try:
                    r = requests.get("https://pselookup.vrymel.com/api/stocks/" + symbol + "/history/" + stockdate)
                    stock = json.loads(r.text)
                    trading_date = stock["history"]["trading_date"]
                    low = stock["history"]["low"]
                    open = stock["history"]["open"]
                    close = stock["history"]["close"]
                    high = stock["history"]["high"]
                    volume = int(stock["history"]["volume"])
                    
                    try:
                        r = requests.get("http://phisix-api.appspot.com/stocks/" + symbol + ".json")
                        stock = json.loads(r.text)

                        pctchange = float(stock["stock"][0]["percent_change"])
                        if int(close) > 1 and int(close) <= 10:
                            change = round(int(close) - (int(close) / (1 + (pctchange/100))) ,3)
                        elif int(close) > 10:
                            change = round(int(close) - (int(close) / (1 + (pctchange/100))),2)
                        else:
                            change = round(int(close) - (int(close) / (1 + (pctchange/100))),4)
        
                        end = timer()
                        time = str(round(end - start, 3)) + "s"
                    except:
                        pctchange = ''
                        change = ''
                        end = timer()
                        time = str(round(end - start, 3)) + "s"
                except:
                    return render(request, 'home/error.html')
                
                try:
                    description = stockdesc[symbol]
                    shortdesc = description[0:200]
                    fulldesc = description[200:]
                    data = fullstockdata[symbol]
                    dict_ver = dict(zip(labels,data))
                    
                    data1 = dict(list(dict_ver.items())[:12])
                    data2 = dict(list(dict_ver.items())[12:24])
                    data3 = dict(list(dict_ver.items())[24:31])
                    data4 = dict(list(dict_ver.items())[31:38])
                    #not included lasttwo elements
                    data5 = dict(list(dict_ver.items())[38:45])
                except:
                    description = ''
                    shortdesc = ''
                    fulldesc = ''
                    data = ''
                    dict_ver = ''
                    data1 = {}
                    data2 = {}
                    data3 = {}
                    data4 = {}
                    data5 = {}
                
                return render(request, 'home/stock.html', 
                {'symbol': symbol, 'name': company_name, 'date': trading_date, 'desc': fulldesc,
                'shortdesc': shortdesc, 'low': low, 'open': open, 'close': close, 'high': high, 'volume': volume,
                'time': time, 'stockdict': stockdict, 'pctchange' : pctchange, 'change' : change,
                'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5 })
                

def chart(request):
    return render(request, 'home/chart.html')

def about(request):
    return render(request, 'home/about.html')


def isweekday(date):
    month = date[0]
    day = date[1]
    year = date[2]

    date[0] = str(date[0])
    date[1] = str(date[1])
    date[2] = str(date[2])
    print(date)
    print(calendar.weekday(year,month,day))
    if calendar.weekday(year,month,day) == 5:
        yesterday = date.now() - timedelta(days=2)
        date= yesterday.strftime('%m%d%y')
        newdate = '20' + date[4:6] + date[0:2]+ date[2:4]
        return newdate
    elif calendar.weekday(year,month,day) == 6:
        yesterday = datetime.today() - timedelta(days=3)
        print(yesterday)
        date= yesterday.strftime('%m%d%y')
        newdate = '20' + date[4:6] + date[0:2] + date[2:4]
        print('ffe')
        return newdate
    if len(date[0]) < 2:
        date[0] = "0" + date[0]
    if len(date[1]) < 2:
        print(date[1])
        date[1] = "0" + date[1]
    newdate = date[2]+date[0]+date[1]
    return newdate