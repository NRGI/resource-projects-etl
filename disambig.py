"""

Currently requires the environment variable DBA_PASS for the password of the
dba user on the virtuoso server. e.g.
    DBA_PASS=dba python disambig.py

"""

import requests
from requests.auth import HTTPDigestAuth
import os


base_uri = 'http://bjwebb.pagekite.me/'
 

def escape(s):
    mapping = {
        '"': '\\"',
        '\r': '\\r',
        '\n': '\\n',
        '\t': '\\t',
        '\b': '\\b',
        '\f': '\\f',
    }
    s = s.replace('\\', '\\u005C\\u005C')
    for key, value in mapping.items():
        s = s.replace(key, value)
    return '"' + s + '"'


def sparql_query(query, default_graph_uri=base_uri + 'tmp'):
    r = requests.post('http://localhost:8890/sparql-auth',
        auth=HTTPDigestAuth('dba', os.environ['DBA_PASS']),
        data={
            'query': query,
            'default-graph-uri': default_graph_uri,
            'format': 'application/sparql-results+json'
        }
    )
    try:
        return r.json()
    except ValueError:
        print(r.text)
 

def disambig_projects():
    query = """
        select ?name (count(?s) as ?projects) where {
            ?s rdf:type <""" + base_uri + """t/project> .
            ?s foaf:name ?name .
        }
        group by (?name)
        having (count(?s) > 1)
    """
    for result in sparql_query(query)['results']['bindings']:
        disambig_project_by_name(result['name']['value'])


def disambig_project_by_name(name):
    query = """
        select ?s where {
            ?s foaf:name """ + escape(name) + """ .
        }
    """
    results = sparql_query(query)['results']['bindings']
    first_result = results[0]
    for result in results[1:]:
        print(result)
        triple = '<{}> <http://www.w3.org/2002/07/owl#sameAs> <{}>'.format(first_result['s']['value'], result['s']['value'])
        input_query = """
            insert data {
                """ + triple + """
            }
        """
        sparql_query(input_query, default_graph_uri=base_uri + 'tmp')


if __name__ == '__main__':
    disambig_projects()
