import pandas as pd
from data_to_pandas import data_frames
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF


combined_df = pd.concat(data_frames)


base_uri = 'http://bjwebb.pagekite.me/'


g = Graph()


type_company = URIRef(base_uri + 't/company')
type_project = URIRef(base_uri + 't/project')
type_location = URIRef(base_uri + 't/location')
type_contract = URIRef(base_uri + 't/contract')
type_license = URIRef(base_uri + 't/license')
type_particiation = URIRef(base_uri + 't/participation')


for line, row in combined_df.iterrows():
    # remove null values from the row
    row = row.dropna()
    source = row['source']

    source_base_uri = '{}s/{}'.format(base_uri, source)
    subject_uri = '{}/{}'.format(source_base_uri, line[1])
    subject = URIRef(subject_uri)

    if source in ['indonesia-eiti-projects']:
        g.add((subject, RDF.type, type_particiation))
    elif source in ['indonesia-mining-licenses', 'indonesia-openoil-concessions', 'rp.org-sources']:
        g.add((subject, RDF.type, type_license))
    elif source in ['indonesia-openoil-contracts']:
        g.add((subject, RDF.type, type_contract))
    #elif source in ['usgs']:
    # I'm not sure what type of thing each row in the usgs spreadsheet corresponds to

    project = URIRef('{}/project'.format(subject_uri))
    g.add((subject, URIRef(base_uri + 'p/project'), project))
    g.add((project, RDF.type, type_project))
    if 'project_name' in row:
        g.add((project, FOAF.name, Literal(row['project_name'])))

    company = URIRef('{}/company'.format(subject_uri))
    g.add((subject, URIRef(base_uri + 'p/company'), company))
    g.add((company, RDF.type, type_company))
    if 'company_name' in row:
        g.add((company, FOAF.name, Literal(row['company_name'])))

    for k, v in row.items():
        if k in ['project_name', 'project_name']:
            continue
        g.add((subject, URIRef(base_uri + 'p/' + k), Literal(v)))


g.serialize(destination='resource-projects.rdf')
g.serialize(format='turtle', destination='resource-projects.turtle')
