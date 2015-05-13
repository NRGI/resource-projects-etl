#!/bin/bash
set -e

mkdir -p data
cd data
wget "http://mrdata.usgs.gov/mineral-operations/minfac-csv.zip"
unzip minfac-csv.zip
rm minfac-csv.zip
cd ..

mkdir -p data/indonesia
cd data/indonesia
wget "https://docs.google.com/spreadsheets/d/1-bmcS2GdS8l2XTXcAlfMyEruDJGGqVBJ87-zmgAExcs/export?format=xlsx" -O 1-indonesia-eiti-projects.xlsx
#mv ../minfac.csv 2-usgs.csv
wget "http://repository.openoil.net/wiki/Special:Ask/-5B-5Btype::Concession-5D-5D-0A-20-5B-5BJurisdiction::Indonesia-5D-5D/-3FConcessionName/-3FConcessionContractor/-3FConcessionDescription/-3FConcessionSource-23-2D/-3FConcessionSourceDate/-3FRetrieved-20at/format%3DCSV/limit%3D5000/mainlabel%3D-2D/default%3D/offset%3D0" -O 3-openoil-concessions-indonesia.csv
wget "http://repository.openoil.net/w/index.php?title=Special%3AAsk&q=%5B%5BCategory%3AContract%5D%5D%0D%0A+%5B%5BJurisdiction%3A%3AIndonesia%5D%5D&po=%3FContract%0D%0A%3FContractType%0D%0A%3FContractor%0D%0A%3FSignatureDate%23MEDIAWIKI%0D%0A%3FHostGovernmentContract%0D%0A%3FLanguage%0D%0A%3FSummary+source+url+plain%0D%0A%3FLocalStoreURLPlain%0D%0A&eq=yes&p%5Bformat%5D=csv&sort_num=&order_num=ASC&p%5Blimit%5D=20&p%5Boffset%5D=0&p%5Blink%5D=all&p%5Bsort%5D=&p%5Bheaders%5D=show&p%5Bmainlabel%5D=-&p%5Bintro%5D=&p%5Boutro%5D=&p%5Bsearchlabel%5D=more+contracts...&p%5Bdefault%5D=No+published+contracts+available+for+this+country.&p%5Bsep%5D=%2C&p%5Bfilename%5D=result.csv&eq=yes" -O 4-openoil-contracts-indonesia.csv
cd ../../

mkdir -p data/drc
cd data/drc
wget "https://docs.google.com/spreadsheets/d/1nnCeutWYNVugb8Tgl7gdItJWL9PBE6XWttXnhv3Shgk/export?format=xlsx" -O 2-rp.org-sources.xlsx
