#!/bin/bash
set -e
docker build -t opendataservices/resource-projects-etl .
docker rm -f virtuoso-etl-test || true
docker rm -f etl-test || true
docker run -d -p 127.0.0.1:8886:8890 --name virtuoso-etl-test opendataservices/virtuoso:master
sleep 30s
cat virtuoso_setup.sql |  docker run --link virtuoso-etl-test:virtuoso -i --rm opendataservices/virtuoso:master isql virtuoso
docker run -d --publish=127.0.0.86:80:80 --link virtuoso-etl-test:virtuoso -e DBA_PASS=dba --name etl-test opendataservices/resource-projects-etl
SERVER_URL=http://127.0.0.86/ SPARQL_ENDPOINT=http://localhost:8886/sparql py.test fts
