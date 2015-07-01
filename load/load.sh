cd /usr/local/var/lib/virtuoso/db/
rm -r import
mkdir import
cp /usr/src/app/data/* import
isql virtuoso dba dba /import.sql
