from data_to_pandas import combined_df
from rdflib import Graph, URIRef, Literal

g = Graph()
for i, row in combined_df.iterrows():
    subject = URIRef('http://localhost/s/'+row['source']+'/'+str(i))
    for k,v in row.dropna().items():
        g.add( (subject, URIRef('http://localhost/p/'+k), Literal(v) ) )

g.serialize(destination='resource-projects.rdf')
g.serialize(format='turtle', destination='resource-projects.turtle')
