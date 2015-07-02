# Company Match

This folder will contain scripts that:

* Load in a list of companies either from local files or SPARQL
* Check against the Open Corporates API for matches
* Pull in data from Open Corporates


## Process

First get a list of company URLs, names and any other information we can obtain about them, to result in a spreadsheet of the format:

| URL | Label | country | operationsIn | activeOn |
|-----|-------|---------|--------------|----------|

The command below using [roqet](http://librdf.org/rasqal/roqet.html) should generate an appropriate input file:

```
roqet -q -i sparql company-list.sparql -r csv -D ../../data/eiti-projects.ttl
```

Or run the SPARQL against the web endpoint. 


The data can then be loaded into Open Refine, when the following processes should be run.


## Exploring corporate groupings
(1) Search the Open Corporates API by names for Company Groupings by applying [groupings.json](refine/groupings.json) in refine.

This will leave a Groupings column which contains any group names identified from the Open Corporates API. Add a text facet on this, and review the groupings that have been found. 

(2) Use the 'edit' option for a column to remove mis-matched groupings: **there are likely to be a number of false positives**, or cases with multiple results, as we search on the first name of the company only. 

To lookup a grouping on the Open Corporates site and confirm it is the correct grouping to use, go to https://opencorporates.com/corporate_groupings/

(3) Once you have removed all invalid groupings, run [oc-group.json](refine/oc-group.json) to set the identifiers these groups.

(4) You can now add further grouping names to the 'Groupings' column, should you wish to create extra groups. Take care to search the ResourceProjects.org platform for the names and identifiers of existing groups when doing this. 

## Fetching company identifiers

(1) Reconcile the data against the Open Corporates Google Reconciliation endpoint by name

At this stage it is important to choose whether to use jurisdiction restrictions or not. 

* reconcile-restricted.json (ToDo) will use the country code value of the country column to look only for companies registered in this jurisdiction, and will use activeOn to affect the scoring of the data
* [reconcile-unrestricted.json](refine/reconcile-unrestricted.json) - will match globally based on names only

(Note: May require reconciliation to be run manually - as reconcile-unrestricted.json did not apply correctly in testing)

Once data is returned, user input is needed to confirm the matches. Care should be taken to **only confirm a match when you are certain that you are identifying the correct legal entity**. For example, ensure that the ResourceProjects company is the same legal entity as the Open Corporates entity you are matching against. Checking the jurisdiction and dates of both can help with this. 

Performing this matching might require in-depth research.

(2) Extract any additional Company Grouping information

Once the match is complete, run [extract-company-data.json](refine/extract-company-data.json) to get the Open Corporates URI for the company, and to look up additional information from this. 

Check the data that has been supplied, and remove any data which you do not wish reflected in the final output.

(3) Clean up ready for import

Then run [clean-for-import.json](refine/clean-for-import.json)

## Export and transform

Export the data to data/company-map.csv

Run ```python transform.py```


## ToDo

Improve query to handle for:

* Cases where there is already a resolved company ID
* Getting the countries in which a company has a stake

Add queries for:

* Companies with no names