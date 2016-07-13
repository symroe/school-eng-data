DATE:=$(shell date +"%Y%m%d")
EDUBASE_URL=http://www.education.gov.uk/edubase/edubasealldata$(DATE).csv

DATA=\
	data/school/schools.tsv\
	$(SCHOOL_DATA)\
	$(ADDRESS_DATA)

SCHOOL_DATA=\
	data/denomination/denominations.tsv\
	data/diocese/dioceses.tsv\
	data/school-federation/school-federations.tsv\
	data/school-phase/school-phases.tsv\
	data/school-type/school-types.tsv

ADDRESS_DATA=\
	data/address/addresses.tsv\
	data/street/streets.tsv

MAPS=\
	maps/addresses.tsv\
	maps/denomination.tsv\
	maps/diocese.tsv\
	maps/school-gender.tsv\
	maps/school-phase.tsv\
	maps/school-type.tsv

all:: flake8 $(DATA)

data/school/schools.tsv: bin/schools.py cache/edubase.csv $(MAPS)
	@mkdir -p data/school
	bin/schools.py < cache/edubase.csv > $@

# extract school addresses from address-data
data/address/addresses.tsv:	bin/addresses.py data/school/schools.tsv
	@mkdir -p data/address
	bin/addresses.py < data/school/schools.tsv > $@

# extract school streets from address-data
data/street/streets.tsv:	bin/streets.py data/address/addresses.tsv
	@mkdir -p data/street
	bin/streets.py < data/address/addresses.tsv > $@


# download from EDUBASE
# - contains invalid UTF-8 characters ..
cache/edubase.csv:
	@mkdir -p cache
	curl -s $(EDUBASE_URL) | iconv -f ISO-8859-1 -t UTF-8 > $@


init::
	pip3 install -r requirements.txt

flake8:
	flake8 --max-line-length=109 bin

prune::
	rm -rf cache
	rm -rf data/school

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
