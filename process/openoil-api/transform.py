import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../../modules/'))
from taglifter import TagLifter

## Note, we're currently using a customised version of the data, not the full data
tl = TagLifter(ontology = "../../ontology/resource-projects-ontology.rdf",source = "source.csv",base="http://resourceprojects.org/",source_meta={})
tl.build_graph()
tl.load_data("data/openoil.csv")
tl.build_graph()

tl.graph.serialize(format='turtle',destination="../../data/openoil.ttl")
