cd /usr/local/var/lib/virtuoso/db/
rm -r import
mkdir import
cp -r /usr/src/app/data/* import
cp /usr/src/app/ontology/*.rdf import
isql virtuoso dba dba /import.sql
