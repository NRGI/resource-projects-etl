import pyodbc
cnxn = pyodbc.connect('DRIVER={VOS};HOST=virtuoso;PORT=111;UID=dba;PWD=dba')
cursor = cnxn.cursor()

