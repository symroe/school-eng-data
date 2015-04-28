# the list of schools is OGL, and public:
# http://www.education.gov.uk/edubase/home.xhtml
# but you need an account to download it as CSV from this source:
DATE=`date +"%Y%m%d"`
EDUBASE_URL=http://www.education.gov.uk/edubase/edubase${DATE}.csv

all:: flake8 data/edubase

# The scripts invoked in this makefile will create data for
# 4 registers: School, Address, PostTown and Postcode
#
# This will create files in the data directory that will contain:
#
# an entry for each school
# an entry for each address of school record extracted
# an entry for each post town of address record extracted
# an entry for each postcode of address record extracted

# All of the above is based in edubase data
#

data/edubase: bin/schools.py
	@mkdir -p data/School data/Address data/PostTown data/Postcode
	cat cache/edubase.csv | bin/schools.py data/School data/Address data/PostTown data/Postcode

cache/results.csv:
	@mkdir cache
	curl -o cache/results.csv $(EDUBASE_URL)

# contains invalid UTF-8 characters ..
cache/edubase.csv:	cache/results.csv
	cat cache/results.csv | iconv -f ISO-8859-1 -t UTF-8 > $@
	rm cache/results.csv

clean::
	rm -rf cache
	rm -rf data

#
#  code
#
init::
	pip3 install -r requirements.txt

flake8:
	flake8 bin

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
