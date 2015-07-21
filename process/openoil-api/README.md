# Open Oil API

This script fetches oil concession information from the OpenOil API and converts to the ResourceProjects.org data model.

## Usage

Set an environment variable for your OpenOIL API Key

```
export OPENOIL_API_KEY=<key>
```

Run extract.py and then transform.py

```
python extract.py
python transform.py
```