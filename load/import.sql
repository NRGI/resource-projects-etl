SPARQL CLEAR GRAPH <http://resourceprojects.org/>;
delete from db.dba.load_list;
ld_dir_all('/usr/local/var/lib/virtuoso/db/import', '*', 'http://resourceprojects.org/');
rdf_loader_run();
