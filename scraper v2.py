from bs4 import BeautifulSoup
import requests
import csv
from timeit import default_timer as timer
from datetime import datetime
from stocklist import stockdict

start = timer()

def marketwatch():
    allinfo = ['Symbol', '52 Week Range', 'Market Cap', 'Outstanding Shares', 'Public Float', 'Beta', 
    'Rev per Employee', 'P/E Ratio', 'EPS', 'Yield', 'Dividend', 'Ex-Dividend Date', 'Avg Volume']

    csvfile = open('keydata.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(allinfo)
    count = 0
    for i in stockdict:
        ticker = i

        r = requests.get(f'https://www.marketwatch.com/investing/stock/{ticker}?countrycode=ph&mod=over_search').text
        soup = BeautifulSoup(r, 'lxml')
        try:
            container = soup.find('div', class_ = 'group group--elements left')
            profile = container.find('ul', class_ ='list list--kv list--col50')
            spans = profile.find_all('span', class_ = 'primary')
            
            company_profile = [span.get_text() for span in spans]

            yearrange = company_profile[2]
            marketcap = company_profile[3]
            outstandingshares = company_profile[4]
            publicfloat = company_profile[5]
            beta = company_profile[6]
            employee_rev = company_profile[7]
            pe_ratio = company_profile[8]
            eps = company_profile[9]
            div_yield = company_profile[10]
            div = company_profile[11]
            div_date = company_profile[12]
            volume = company_profile[15]            

            csv_writer.writerow([ticker,yearrange,marketcap,outstandingshares,publicfloat,beta, 
            employee_rev,pe_ratio,eps,div_yield,div,div_date,volume])

        except:
            print(str(i) + " Not found...")


        count += 1
        end = timer()
        time = str(round(end - start, 3))
        print(str(i) + " Parsed successfully   " + str(count) + " /318    Time Elapsed: " + time + "s")
        

    csvfile.close()


marketwatch()