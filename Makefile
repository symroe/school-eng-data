DATE:=$(shell date +"%Y%m%d")
EDUBASE_URL=http://www.education.gov.uk/edubase/edubasealldata$(DATE).csv

REGISTERS=\
	data/school/school.tsv

all:: flake8 $(REGISTERS)

data/school/school.tsv: bin/schools.py cache/edubase.csv
	@mkdir -p data/school
	bin/schools.py < cache/edubase.csv > $@

# download from EDUBASE
# - contains invalid UTF-8 characters ..
cache/edubase.csv:
	@mkdir -p cache
	curl -s $(EDUBASE_URL) | iconv -f ISO-8859-1 -t UTF-8 > $@

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
