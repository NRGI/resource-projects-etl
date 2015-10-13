DB.DBA.RDF_GRAPH_GROUP_CREATE('http://staging.resourceprojects.org/data/', 1);
DB.DBA.RDF_GRAPH_GROUP_CREATE('http://live.resourceprojects.org/data/', 1);
insert into DB.DBA.SYS_SPARQL_HOST (SH_HOST, SH_GRAPH_URI) values ('%live%', 'http://live.resourceprojects.org/data/');
insert into DB.DBA.SYS_SPARQL_HOST (SH_HOST, SH_GRAPH_URI) values ('%staging%', 'http://staging.resourceprojects.org/data/');
