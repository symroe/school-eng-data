DATE:=$(shell date +"%Y%m%d")
EDUBASE_URL=http://www.education.gov.uk/edubase/edubasealldata$(DATE).csv

REGISTERS=\
	data/school/schools.tsv

all:: flake8 $(REGISTERS)

data/school/schools.tsv: bin/schools.py cache/edubase.csv maps/addresses.tsv
	@mkdir -p data/school
	bin/schools.py < cache/edubase.csv > $@

# download from EDUBASE
# - contains invalid UTF-8 characters ..
cache/edubase.csv:
	@mkdir -p cache
	curl -s $(EDUBASE_URL) | iconv -f ISO-8859-1 -t UTF-8 > $@


init::
	pip3 install -r requirements.txt

flake8:
	flake8 bin

prune::
	rm -rf cache
	rm -rf data/school

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
