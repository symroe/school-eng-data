DATE:=$(shell date +"%Y%m%d")
EDUBASE_URL=http://www.education.gov.uk/edubase/edubasealldata$(DATE).csv

REGISTERS=\
	data/school/schools.tsv

DATA=\
	data/diocese/dioceses.tsv\
	data/school-federation/school-federations.tsv\
	data/school-phase/school-phases.tsv\
	data/school-type/school-types.tsv

MAPS=\
	maps/addresses.tsv\
	maps/diocese.tsv\
	maps/school-gender.tsv\
	maps/school-phase.tsv\
	maps/school-type.tsv

all:: flake8 $(REGISTERS)

data/school/schools.tsv: bin/schools.py cache/edubase.csv $(DATA) $(MAPS)
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
	flake8 --max-line-length=109 bin

prune::
	rm -rf cache
	rm -rf data/school

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
