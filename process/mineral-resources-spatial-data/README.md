# Mineral Resources On-Line Spatial Data

Data from http://mrdata.usgs.gov/mineral-operations/

"Mineral facilities and operations outside the United States compiled by the National Minerals Information Center of the USGS."

Notes: 

* The data only goes up to 2007. 

## Process

(1) Run extract.sh to download the full archive of data

(2) Load the data into Open Refine

(3) Run the refine scripts 

(4) Export as CSV into sources/minfac-csv-refined.csv

(5) Run transform.py


## Data strengths and weaknesses

### Strengths

The data indicates firms who had a stake in activities in particular geographic locations in c. 2005 - 2008.

The data provides point locations for sites.

### Weaknesses
The naming of sites in the dataset is very variable - and so should not be relied upon. 

The investment percentages column is not well cleaned. Manual review of the refine files will be needed to get very accurate data.

## Cleaning we carry out

* Not all the facilities have names. Where names are missing, we use the location instead. 
