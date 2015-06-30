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

The output of each process should be written to the root /data/ folder, from where it can be loaded onto the ResourceProjects.org platform.



## Requirements

<strike>Python 3</strike> (Currently needs upgrades to work with Python 3)

### Getting started

```
virtualenv .ve --python=/usr/bin/python3
source .ve/bin/activate
pip install -r requirements.txt
```

