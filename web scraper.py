from bs4 import BeautifulSoup
import requests
import csv
from timeit import default_timer as timer
from datetime import datetime
from stocklist import stockdict

start = timer()

def marketwatch():
    allinfo = ['Ticker','52 Week Range', 'Market Cap', 'Outstanding Shares', 'Public Float', 'Beta', 
    'Rev per Employee', 'P/E Ratio', 'EPS', 'Yield', 'Dividend', 'Ex-Dividend Date', 'Avg Volume',
    'Desc','Industry','Sector','Revenue','Net Income','2020 Sales Growth','Employees',
    'P/E Current', 'Extraordinary', 'No extraordinary', 'Sales Ratio','Book Ratio','Cashflow Ratio',
    'EV EBITDA','EV Sales', 'Debt to EV','Employee Revenue', 'Employee Income', 'Receivable Turnover', 'Total Turnover',
    'Current Ratio', 'Quick Ratio', 'Cash Ratio',
    'Gross Margin', 'Operationg Margin', 'Pretax Margin', 'Net Margin',
    'Return on Assests', 'Return on Equity', 'Return on Total Capital', 'Return on Invested Capital',
    'Debt to Equity', 'Debt to Capital', 'Debt to Assets', 'Longterm Debt to Equity', 'Longterm Debt to Capital']

    csvfile = open('stockinfo.csv', 'w', newline='', encoding='utf-8')
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

            r = requests.get(f'https://www.marketwatch.com/investing/stock/{ticker}/company-profile?countrycode=ph&mod=mw_quote_tab').text
            soup = BeautifulSoup(r, 'lxml')
            try:
                container = soup.find('div', class_ = 'container container--body')
                profile = container.find('ul', class_ ='list list--kv list--col50')
                desc = container.find('p', class_ = 'description__text').text
                spans = profile.find_all('span', class_ = 'primary')
                
                company_profile = [span.get_text() for span in spans]
                industry = company_profile[0]
                sector = company_profile[1]
                revenue = company_profile[3]
                netincome = company_profile[4]
                salesgrowth2020 = company_profile[5]
                employees = company_profile[6]

                table = container.find_all('table' , class_ = 'table value-pairs no-heading')
                cells0 = table[0].find_all(True, {'class':['table__cell w25', 'table__cell w25 is-na']})
                
                valuation = [cell.get_text() for cell in cells0]

                pe_current = valuation[0]
                extra = valuation[1]
                no_extra = valuation[2]
                salesratio = valuation[3]
                bookratio = valuation[4]
                cashflow = valuation[5]
                ev_ebitda = valuation[6]
                ev_sales = valuation[7]
                ev_debt = valuation[8]

                cells1 = table[1].find_all(True, {'class':['table__cell w25', 'table__cell w25 is-na']})

                efficiency = [cell.get_text() for cell in cells1]
                revenue_emp = efficiency[0]
                income_emp = efficiency[1]
                received_turnover = efficiency[2]
                total_turnover = efficiency[3]

                cells2 = table[2].find_all(True, {'class':['table__cell w25', 'table__cell w25 is-na']})
                
                liquidity = [cell.get_text() for cell in cells2]
                current_ratio = liquidity[0]
                quick_ratio = liquidity[1]
                cash_ratio = liquidity[2]

                cells3 = table[3].find_all(True, {'class':['table__cell w25', 'table__cell w25 is-na']})
                
                profitability = [cell.get_text() for cell in cells3]

                gross_margin = profitability[0]
                operating_margin = profitability[1]
                pretax_margin = profitability[2]
                net_margin = profitability[3]
                returnon_assests = profitability[4]
                returnon_equity = profitability[5]
                returnon_total = profitability[6]
                returnon_invested = profitability[7]

                cells4 = table[4].find_all(True, {'class':['table__cell w25', 'table__cell w25 is-na']})

                capitalization = [cell.get_text() for cell in cells4]

                debt_to_equity = capitalization[0]
                debt_to_capital = capitalization[1]
                debt_to_assets = capitalization[2]
                longdebt_equity = capitalization[3]
                longdebt_capital = capitalization[4]

                csv_writer.writerow([
                ticker,yearrange,marketcap,outstandingshares,publicfloat,beta, 
                employee_rev,pe_ratio,eps,div_yield,div,div_date,volume,
                desc,industry,sector,revenue,
                netincome,salesgrowth2020,employees,
                pe_current,extra,no_extra,salesratio,bookratio,cashflow,ev_ebitda,ev_sales,ev_debt,
                revenue_emp,income_emp,received_turnover,total_turnover,
                current_ratio,quick_ratio,cash_ratio,
                gross_margin,operating_margin,pretax_margin,net_margin,
                returnon_assests,returnon_equity,returnon_total,returnon_invested,
                debt_to_equity,debt_to_capital,debt_to_assets,longdebt_equity,longdebt_capital])

            except:
                csv_writer.writerow([
                ticker,yearrange,marketcap,outstandingshares,publicfloat,beta, 
                employee_rev,pe_ratio,eps,div_yield,div,div_date,volume])
        except:
            print(str(i) + " Not found...")


        count += 1
        end = timer()
        time = str(round(end - start, 3))
        print(str(i) + " Parsed successfully   " + str(count) + " /318    Time Elapsed: " + time + "s")
        

    csvfile.close()

marketwatch()
