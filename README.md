# resource-projects-etl

This repository contains a library for Extract, Transform and Load processes for ResourceProjects.org.

You can report issues with current transformations, or suggest sources which should be added to this library using the GitHub issue tracker.


## Processes
Each process, located in the **process** folder consists of:

* A README.md file describing the transformation
* An extract.sh or extract.py file to fetch the file
* A data/ subfolder where the extracted data is stored
* A transform.py file which runs the transformations
* A meta.json file, containing the meta-data which transform.py will use

The output of each process should be written to the /data/ folder, from where it can be loaded onto the ResourceProjects.org platform.



## Requirements

Python 3

### Getting started

```
virtualenv .ve --python=/usr/bin/python3
source .ve/bin/activate
pip install -r requirements.txt
```

