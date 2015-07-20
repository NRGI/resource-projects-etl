# Commodity codelist

The process in this folder describes how to map a list of commodities to the [UN Central Product Classification (CPC) Version 2](http://unstats.un.org/unsd/cr/registry/cpc-2.asp)

It can be used to set-up a CSV reconciliation endpoint, using [Reconcile CSV](http://okfnlabs.org/reconcile-csv/) against the CPC V 2. database.

## Related issues: 

* [ResourceProjects.org #19](https://github.com/NRGI/resourceprojects.org/issues/19)

## Usage

(1) Run endpoint.sh to download and run the reconcilation endpoint

(2) In [Open Refine](http://openrefine.org/) create a project with the list of commodity names you want to map

(3) Against the column of commodity names, choose 'Reconcile > Start Reconciling'. 

(4) If this is the first time you have carried out a CSV reconciliation, choose 'Add standard service' and enter ```http://localhost:8000/reconcile/``` as the address;

(5) Run the reconciliation process;

(6) Review the reconciliation to look for matches and set them;

(7) Add a new column based on the reconciled column, with the grel expression ```cell.recon.match.id``` to extract the code.

