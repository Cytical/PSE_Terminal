import csv

def dictdata():
    with open(r'C:\Users\guiao\PSE_Terminal\pseindex.csv', mode='r',encoding='utf8') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            ticker = rows[1].replace('PSE:', '')
            print(f"'{ticker}': '{rows[0]}',")

def dictdesc():
    with open(r'C:\Users\guiao\PSE_Terminal\stockinfofinal.csv', mode='r',encoding='utf8') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            print(f"'{rows[0]}':")
            #strip = rows[13].replace("'","\'")
            print(f"'''{rows[13]}''',")
            print()

dictdata()
#dictdesc()