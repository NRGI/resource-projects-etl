# StatOil Annual Reports

This documents a manual conversion process.

Data has been scraped by NRGI from the StatOil reports and is available at https://docs.google.com/spreadsheets/d/16YS6-3r9iPzxqY0CJJChdEppSAjybDSXk5l67lGf2AA/edit#gid=1542370502

Preparing this data involves:

* Reconciliation against the OpenCorporates API to identify companies
* Manually renaming projects based on best-efforts and cross-referencing Open Oil block data


## Process

(1) Download the 'Consolidated project overview (not in report)' sheet to sources/statoil-2014-project-overview.csv

(2) Load sources/statoil-2014-project-overview.csv into [Open Refine](http://openrefine.org/)

(3) Run the actions defined in refine.json against the file

(4) Export the results as CSV to sources/statoil-2014-project-overview-refined.csv

(5) Upload into online template at https://docs.google.com/spreadsheets/d/1ZOPwbn98xlccJ01uDXIRNxPxQAnWJ99bQTtpelSuyEY/edit#gid=21324452 and manually curate data

(6) Run the google-docs-transform.py script against this spreadsheet. 





