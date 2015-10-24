# TagLifter

Tag Lifter takes a spreadsheet of data, marked up with #tag headings for columns, and converts this to a Linked Data graph based on an ontology.

Tags may take the following forms:

| N | Tag | Interpretation |
|---|-----|----------------|
| 1 | #class | Create a new entity with the value of this column as skos:PrefLabel | 
| 2 | #class+**identifier** | Use the value of this column as the identifier of any #class in this row | 
| 3 | #class+dataProperty | Use the value of this column as the literal value of the data property of the class entity |
| 4 | #class+class | Look for a **direct** relationship between the two classes (in either direction **NOT CURRENTLY IMPLEMENTED**), and assert the objectProperty between the two classes. If no direct relationship exists, look for an intermediate step and establish this relationship instead. |
| 5 | #class+class+dataProperty | See if the dataProperty can attach to the second class and if so, attach it. If not, see if there was an intermediate entity created to join the two classes, and if the dataProperty can attach to this, add it here. |

In addition, tags may include:

**+n** to distinguish two instances of the same class or data property in the same row. For example, #project+1 and #project+2

**+en** or any other two-digit country code to indicate the language that should be applied to any string literals created for that column. 

To parse spreadsheets Tag Lifter will:

- Read left-to-right across each row;
- Whenever it encounters a new class, check to see if any subsequent column contains a name and identifier for this;
- Check for relationships between any classes at the same level of the tag hierarchy;
- Cache identifiers for entities; 

When reading a multiple tabbed spreadsheet, TagLifter will cache the identifiers for any named entity. For example, once it has established an identifier for a #project named 'Jubilee', it will use this identifier on future sheets for rows containing a #project column where the cell contains 'Jubilee', even if no #project+identifier column is present. 


## Examples

### #Class

Input:

| #project |
|----------|
| Jubilee Fields |

Output:

```
<http://example.net/Project/random-id> a base:Project;
            skos:prefLabel "Jubilee Fields"@en.
```

The ```identifierPattern``` property of each class in the ontology is used to determine how identifiers should be generated if no +identifier column is present. 

### #class+identifier

Identifier is a reserved keyword.

Input:

| #project | #project+identifier |
|----------|---------------------|
| Jubilee Fields | gh/jufi-asd24f |

Output:

```
<http://example.net/Project/gh/jufi-asd24f> a base:Project;
            skos:prefLabel "Jubilee Fields"@en.
```

### #class+dataProperty

Input:

| #source | #source+identifier | #source+url
|----------|---------------------|
| Projects Report |  | http://www.example.com/project-report |

Output:

```
<http://example.net/Source/random-string-asd123> a base:Source;
        skos:prefLabel "Projects Report"@en;
        base:url "http://www.example.com/project-report".
```

### #class+class

#### Direct relationship

Where the ontology allows a direct relationship between the two classes, such as:

``` <Project> base:relatedContract <Contract>```

Input: 

| #project | #project+identifier | #project+contract |
|----------|---------------------|-------------------|
| Jubilee Fields | gh/jufi-asd24f | Jubilee Contract |

Output:

```
<http://example.net/Project/gh/jufi-asd24f> a base:Project;
        skos:prefLabel "Jubilee Fields"@en;
        base:relatedContract <http://example.net/Contract/juco-aw4v82>.

<http://example.net/Contract/juco-aw4v82> a base:Contract;
        skos:prefLabel "Jubilee Contract"@en.
```

#### Indirect relationship

Where an intermediate entity sits between the two classes, such as:

```<Project> hasStake <Stake> hasStakeholder <Company>```

Input:
    
| #project | #project+identifier | #project+company | #project+company+identifier |
|----------|---------------------|-------------------|----------------------------|
| Jubilee Fields | gh/jufi-asd24f | Tullow Oil | gh/tullow-oil |

Output:

```
<http://example.net/Project/gh/jufi-asd24f> a base:Project;
           skos:prefLabel "Jubilee Fields"@en;
           base:hasStake <http://example.net/stake/123fbas5na>.

<http://example.net/stake/123fbas5na> a base:Stake;
        base:hasStakeholder <http://example.net/company/gh/tullow-oil>.

<http://example.net/company/gh/tullow-oil> a base:Company;
        skos:prefLabel "Tullow Oil"@en.
```


### #class+class+dataProperty

#### Direct relationship

Where the ontology allows a direct relationship between the two classes, such as:

``` <Project> base:source <Source>```

Input:

| #project | #project+identifier | #project+source | #project+source+url |
|----------|---------------------|-------------------|----------------------------|
| Jubilee Fields | gh/jufi-asd24f | Project Report | http://www.example.com/project-report |

Output:

```
<http://example.net/Project/gh/jufi-asd24f> a base:Project;
           skos:prefLabel "Jubilee Fields"@en;
           base:source <http://example.net/Source/random-string-asd123>.

<http://example.net/Source/random-string-asd123> a base:Source;
        skos:prefLabel "Projects Report"@en;
        base:url "http://www.example.com/project-report".
```

#### Indirect relationship

Where an intermediate entity sits between the two classes, such as:

```<Project> hasStake <Stake> hasStakeholder <Company>```
    
and the property attaches to the intermediate entity. 

Input:
    
| #project | #project+identifier | #project+company | #project+company+identifier | #project+company+share |
|----------|---------------------|-------------------|----------------------------|------------------------|
| Jubilee Fields | gh/jufi-asd24f | Tullow Oil | gh/tullow-oil | 10 |

Output:

```
<http://example.net/Project/gh/jufi-asd24f> a base:Project;
           skos:prefLabel "Jubilee Fields"@en;
           base:hasStake <http://example.net/stake/123fbas5na>.

<http://example.net/stake/123fbas5na> a base:Stake;
        base:hasStakeholder <http://example.net/company/gh/tullow-oil>;
        base:share 10.
        
<http://example.net/company/gh/tullow-oil> a base:Company;
        skos:prefLabel "Tullow Oil"@en.
```


### #class and #class

Where two classes are next to each other, and then can be related, establish the relationship.

Input: 

| #project | #project+identifier | #company | #company+identifier |
|----------|---------------------|----------|---------------------|
| Jubilee Fields | gh/jufi-asd24f | Tullow Oil | gh/tullow-oil | 

Output:

```
<http://example.net/Project/gh/jufi-asd24f> a base:Project;
           skos:prefLabel "Jubilee Fields"@en;
           base:hasStake <http://example.net/stake/123fbas5na>.

<http://example.net/stake/123fbas5na> a base:Stake;
        base:hasStakeholder <http://example.net/company/gh/tullow-oil>.
        
<http://example.net/company/gh/tullow-oil> a base:Company;
        skos:prefLabel "Tullow Oil"@en.
```

