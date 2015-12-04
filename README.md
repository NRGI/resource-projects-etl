# resource-projects-etl

This repository contains a library for Extract, Transform and Load processes for ResourceProjects.org.

You can report issues with current transformations, or suggest sources which should be added to this library using the GitHub issue tracker.

## Processes
Each process, located in the **process** folder consists of a collection of files that either (a) document a manual transformation of the data; or (b) perform an automated transformation.

Folders may contain:

* A README.md file describing the transformation
* An extract.sh or extract.py file to fetch the file
* A data/ subfolder where the extracted data is stored during conversion (ignored by git)
* A transform.py file which runs the transformations
* A meta.json file, containing the meta-data which transform.py will use
* A prov.ttl file containing provenance information (using [PROV-O](www.w3.org/TR/prov-o)) to be merged into the final graph

The output of each process should be written to the root data/ folder, from where it can be loaded onto the ResourceProjects.org platform.

## Running ETL Dashboard with with docker

### Running from docker hub

You will need [virtuoso container running](https://github.com/NRGI/resourceprojects.org-frontend/#pre-requisites).

```
docker rm -f rp-etl
docker run --name rp-etl --link virtuoso:virtuoso -p 127.0.0.1:8000:80 -e DBA_PASS=dba opendataservices/resource-projects-etl
```

Update DBA_PASS as appropriate.

Then visit http://locahost:8000/

### Full ResourceProjects.org deployment (with data staging and live frontends)

OpenDataServices dev deploy can be found at https://github.com/OpenDataServices/opendataservices-deploy/blob/master/salt/resource-projects.sls (this is a SaltStack state file).

For a live deploy, running docker directly (you probably don't want to do this, but the below commands should be translatable to your preferred deployment approach), you could do:

```
# Create the volume containers
docker create --name virtuoso-data -v /usr/local/var/lib/virtuoso/db opendataservices/virtuoso:live
docker create --name etl-data -v /usr/src/resource-projects-etl/db -v /usr/src/resource-projects-etl/src/cove/media opendataservices/resource-projects-etl:live

# Run the containers
# Virtuoso
docker run -p 127.0.0.1:8890:8890 --volumes-from virtuoso-data --name virtuoso opendataservices/virtuoso:live
# ETL
docker run -p 127.0.0.1:8001:80 --link virtuoso:virtuoso -e "DBA_PASS=dba" -e FRONTEND_LIVE_URL=http://resourceprojects.org/ -e FRONTEND_STAGING_URL=http://staging.resourceprojects.org/ --volumes-from etl-data opendataservices/resource-projects-etl:live
# Frontend (Live)
docker run  -p 127.0.0.1:8080:80 --link virtuoso:virtuoso-live -e BASE_URL=http://resourceprojects.org/  -e SPARQL_ENDPOINT=http://virtuoso-live:8890/sparql -e DEFAULT_GRAPH_URI=http://resourceprojects.org/data/ opendataservices/resourceprojects.org-frontend:live
# Frontend (Staging)
docker run -p 127.0.0.1:8081:80 --link virtuoso:virtuoso-staging -e BASE_URL=http://staging.resourceprojects.org/  -e SPARQL_ENDPOINT=http://virtuoso-staging:8890/sparql -e DEFAULT_GRAPH_URI=http://staging.resourceprojects.org/data/ opendataservices/resourceprojects.org-frontend:live

# Perform initial virtuoso setup
# (this needs running from the directory containing `virtuoso_setup.sql`)
cat virtuoso_setup.sql |  docker run --link virtuoso:virtuoso -i --rm opendataservices/virtuoso:live isql virtuoso
```

If `BASE_URL` does not match the URL the sites are exposed at, site navigation won't work correctly. Similarly for the etl container, `FRONTEND_LIVE_URL` and `FRONTEND_DEV_URL` should be relevant deployed urls.

On the other hand, `SPARQL_ENDPOINT`, `DEFAULT_GRAPH_URI` and the contents of `virtuoso_setup.sql`, should be left exactly as they are here. (`SPARQL_ENDPOINT` relates to urls that are wired up inside the docker container by --link, whereas `DEFAULT_GRAPH_URI` and the contents of `virtuoso_setup.sql` are virtuoso's internal URI's, and don't relate to the URL the site is actually accessible at).

The above commands expose on 8890, 8801, 8080 and 8081 on localhost. Edit these to match what you want, or place a reverse proxy in front of them.

You should update the virtuoso admin password - through the virutoso HTTP user interface, and then in the DBA_PASS environment variable passed to the ETL container.

To get more recent builds than live, replace `:live` with `:master` in the above.


### Performing database migrations

Run this against the etl container (you will need to replace `etl` with the name of your conatiner):

```
docker exec etl manage.py migrate 
```


### Backup data

```
docker run --volumes-from etl-data -v $(pwd):/backup opendataservices/virtuoso:master tar cvzf /backup/etl-data.tar.gz /usr/src/resource-projects-etl/db /usr/src/resource-projects-etl/src/cove/media
```

Restore:
```
docker run -it --volumes-from etl-data -v $(pwd):/backup opendataservices/virtuoso:master tar xvzf /backup/etl-data.tar.gz -C /
```


### Building docker image

```
docker build -t opendataservices/resource-projects-etl .
```

Then run as described above. (You may want to use a different name for your own image, so as not to get confused with those actually from docker hub).

## Running taglifter locally

### Requirements

* Python 3
* Bash

### Run

```
virtualenv .ve --python=/usr/bin/python3
source .ve/bin/activate
pip install -r requirements.txt
./transform_all.sh
```

You will then have some data as Turtle in the data/ directory.

# License

```
Copyright (c) 2015 Natural Resource Governance Institute

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```

Note that some parts of the ETL tooling depend on
[CoVE](https://github.com/OpenDataServices/cove), which is licensed under the
AGPLv3, so must be used in accordance with that license.
