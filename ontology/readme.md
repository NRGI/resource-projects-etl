<p>
    ResourceProjects.org is backed by an <a href="https://en.wikipedia.org/wiki/Web_Ontology_Language">OWL Ontology</a> which describes the kinds of entities (classes) you will find the datastore, their properties, and how they relate to one another. This helps us to capture important features of the resource project landscape, including:
</p>
<p>
<ul>
    <li><strong>Networks of company ownership</strong> - representing companies, and the groups they are part of;</li>
    <li><strong>Change over time</strong>. For example, when the stake a company holds in a project changes from year to year.</li>
</ul>
</p>
<p>
    In order to make it easier to deal with this richly structured data in spreadsheet formats we have also developed a simple tagging language, which makes it possible to mark-up tabular data for import into our data store.
</p>

<h2>Data Tags</h2>

<p>
    Data tags can be placed anywhere in the first 10 rows of a spreadsheet to indicate what each column contains. Anything above the tag row will be ignored when data is imported, allowing you to include local language field-names, notes and explanations in the top rows of the spreadsheet. 
</p>

Tags are made up of a number of parts, separated by '+'.

<h2>Objects</h2>

The first part of a tag, or a single part tag, should match one of the classes contained in the ontology. 

It indicates that the column describes objects of that class. 

If the class name is the only, or last part, of the tag, then the column contains names for these objects. 

For example, a column tagged #project indicates that cells in that column give the names of projects.

Objects are assigned an ID the first time they are encountered in a spreadsheet. First, the conversion script checks for an identifier property of the object (.e.g a column labelled #project+identifier), but if this cannot be found, or is blank, it assigns a new identifier based on a pattern defined in the ontology. 

<h2>Properties</h2>

If the object part of a tag is followed by a valid data property of that class, then the column is taken to represent that property of the object.

For example, startDate is a datetime property that can be attached to Project objects. The tag #project+startDate indicates that the column contains the startDate for the project in that row. 

<h2>Relationships</h2>

If two class names are found next to each other in a tag, then the column indicates a relationship between objects of these classes.

For example, #project+company indicates that the column (a) contains a company name; (b) that this company is related to a project (which was probably named in an earlier column tagged #project). 

Here, the conversion script is designed to help allow complex relationships to be expressed concisely. For example, in our ontology, project and company cannot be <em>directly</em> related to each other. Instead, companies may hold stakes, and stakes are in projects. This helps us to model change over time (a stake can have a start and end date).

This means that the conversion script looks for both <strong>direct</strong> relationships between two classes, and asserts an objectProperty relationship between two objects, <em>or</em>, if no direct relationship can be found, it looks for a relationship at one-step remove and then: (a) creates the intermediate object; (b) asserts the relevant objectProperties to complete the chain. In these cases, it also checks if any subsequent properties found should be attached to the explicitly named object (e.g. Company in our example), or the intermediate object (e.g. Stake) based on the valid properties according to the ontology. 

