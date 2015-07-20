echo "Setting up reconciliation endpoint at http://localhost:8000 against UN CPC"
wget http://okfnlabs.org/reconcile-csv/dist/reconcile-csv-0.1.2.jar
wget http://unstats.un.org/unsd/cr/registry/regdntransfer.asp?f=130
unzip regdntransfer.asp?f=130
rm regdntransfer.asp?f=130
java -Xmx2g -jar reconcile-csv-0.1.2.jar CPC_Ver_2_english_structure.txt Description Code