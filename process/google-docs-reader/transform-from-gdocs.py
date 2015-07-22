import sys, os
import re 
import requests
import json
sys.path.insert(1, os.path.join(sys.path[0], '../../modules/'))
from taglifter import TagLifter
from rdflib import Graph
import requests


sheets_to_parse = ['Sources','Companies and Groups','Projects, sites & companies','Payments','Production']

tl = TagLifter(ontology = "../../ontology/resource-projects-ontology.rdf",base="http://resourceprojects.org/",source_meta={})

gdoc = str(sys.argv[1])
output = str(sys.argv[2])
result = re.search("([-\w]{25,})", gdoc)
key = result.group(0)

sheetlist = requests.get('https://spreadsheets.google.com/feeds/worksheets/'+key+'/public/full?alt=json')

sheetjson = json.loads(sheetlist.text)

for entry in sheetjson['feed']['entry']:
    if entry['title']['$t'] in sheets_to_parse:
        for link in entry['link']:
            if link['type'] == "text/csv":
                print(link['href'])
                print("Loading " + entry['title']['$t'])
                tl.source_meta = {"sheet":entry['title']['$t']}
                tl.load_data(link['href'])
                tl.build_graph()

tl.graph.serialize(format='turtle',destination="../../data/"+output +".ttl")
                
