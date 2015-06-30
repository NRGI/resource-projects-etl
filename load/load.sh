cd /usr/local/var/lib/virtuoso/db/
rm -r import
mkdir import
cp /data/* import
isql virtuoso dba dba /import.sql
