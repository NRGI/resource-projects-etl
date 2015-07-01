import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../../modules/'))
from taglifter import TagLifter

## Note, we're currently using a customised version of the data, not the full data
tl = TagLifter(ontology = "../../ontology/resource-projects-ontology.rdf",source = "sources/minfac-csv-refined.csv",base="http://resourceprojects.org/",
            source_meta={})

#tl.limit_rows = 5
tl.build_graph()

print(tl.graph.serialize(format='turtle',destination="../../data/minfac-mining-sites.ttl"))

