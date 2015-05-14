import pandas as pd
from data_to_pandas import data_frames
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF


combined_df = pd.concat(data_frames)

base_uri = 'http://bjwebb.pagekite.me/'

g = Graph()
company_type = URIRef(base_uri+'t/company')
project_type = URIRef(base_uri+'t/project')
for line, row in combined_df.iterrows():
    row = row.dropna()

    subject_uri = '{}s/{}/{}'.format(base_uri, *line)
    subject = URIRef(subject_uri)

    project = URIRef('{}/project'.format(subject_uri))
    g.add((subject, URIRef(base_uri+'p/project'), project))
    g.add((project, RDF.type, project_type))
    if 'project_name' in row:
        g.add((project, FOAF.name, Literal(row['project_name'])))

    company = URIRef('{}/company'.format(subject_uri))
    g.add((subject, URIRef(base_uri+'p/company'), company))
    g.add((company, RDF.type, company_type))
    if 'company_name' in row:
        g.add((company, FOAF.name, Literal(row['company_name'])))

    for k, v in row.items():
        if k in [ 'project_name', 'project_name' ]:
            continue
        g.add((subject, URIRef(base_uri+'p/'+k), Literal(v)))


g.serialize(destination='resource-projects.rdf')
g.serialize(format='turtle', destination='resource-projects.turtle')
