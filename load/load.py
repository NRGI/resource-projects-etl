import pyodbc
cnxn = pyodbc.connect('DRIVER={VOS};HOST=virtuoso;PORT=111;UID=dba;PWD=dba')
cursor = cnxn.cursor()
cursor.execute('SPARQL select ?g where {GRAPH ?g{?s a ?t}};')
