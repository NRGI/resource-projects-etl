import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../../modules/'))
from taglifter import TagLifter

## Note, we're currently using a customised version of the data, not the full data
tl = TagLifter(ontology = "../../ontology/resource-projects-ontology.rdf",source = "data/company-map.csv",base="http://resourceprojects.org/",
            source_meta={})

tl.build_graph()

print(tl.graph.serialize(format='turtle',destination="../../data/company-map.ttl"))
