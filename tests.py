from bs4 import BeautifulSoup
import requests
import csv
from timeit import default_timer as timer
from datetime import datetime
import json
#from stocklist import stockdict

now = datetime.now()
time = int(now.strftime("%H").strip('0'))

if time > 12:
    print('wgnwi')
else:
    print('wbgueg')

