import pandas as pd
from data_to_pandas import data_frames
from rdflib import Graph, URIRef, Literal


combined_df = pd.concat(data_frames)


g = Graph()
for line, row in combined_df.iterrows():
    subject = URIRef('http://localhost/s/{}/{}'.format(*line))
    for k,v in row.dropna().items():
        g.add( (subject, URIRef('http://localhost/p/'+k), Literal(v) ) )


g.serialize(destination='resource-projects.rdf')
g.serialize(format='turtle', destination='resource-projects.turtle')
