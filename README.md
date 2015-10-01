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
