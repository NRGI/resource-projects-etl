import os
import sys
import requests
from collections import OrderedDict
import csv

try:
    api_key = os.environ['OPENOIL_API_KEY']
except KeyError:
    print("No API key found in the OPENOIL_API_KEY environment variable")    
    sys.exit()

output = []
page = 1

r = requests.get("http://api.openoil.net/v0.1/concession/search?page="+str(page)+"&apikey="+api_key)
maxn = 0
last_page = False


while last_page == False:
    for result in r.json()['results']:
        line = {"#source":"OpenOilAPI",
                "#source+1":result['source_document'],
                "#source+1+retrievedDate":result['retrieved_date'],
                "#source+1+sourceDate":result['source_date'],
                "#source+1+url":result['url_api'],
                "#country":result['country'],
                "#license":result['name'],
                "#license+identifier":result['identifier']}
        n = 0
        for company in result['licensees']:
            n += 1
            line['company+'+str(n)] = company

        if(n > maxn): 
            maxn = n

        output.append(line)
    
    if (int(r.json()['page']) * 100) > int(r.json()['result_count']):
        last_page= True
    else:
        page += 1
        print("Fetching page "+ str(page))
        r = requests.get("http://api.openoil.net/v0.1/concession/search?page="+str(page)+"&apikey="+api_key)
        
    

keys = ["#source","#source+1","#source+1+retrievedDate","#source+1+sourceDate","#source+1+url","#country","#license","#license+identifier"]
for x in range (0,maxn):
    keys.append("company+"+str(x))

f = open('data/openoil.csv','wt')
w = csv.DictWriter(f,keys,extrasaction='ignore')
w.writeheader()
w.writerows(output)
f.close()
