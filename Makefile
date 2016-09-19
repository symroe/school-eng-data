DATE:=$(shell date +"%Y%m%d")
EDUBASE_URL=http://www.education.gov.uk/edubase/edubasealldata$(DATE).csv

DATA=\
	data/discovery/school-eng/schools.tsv\
	data/discovery/school-wls/schools.tsv\
	data/alpha/school-eng/schools.tsv\
	$(SCHOOL_DATA)\
	$(ADDRESS_DATA)

SCHOOL_DATA=\
	data/discovery/religious-character/religious-characters.tsv\
	data/discovery/diocese/dioceses.tsv\
	data/discovery/school-federation/school-federations.tsv\
	data/discovery/school-phase/school-phases.tsv\
	data/alpha/school-trust/school-trusts.tsv\
	data/discovery/school-type/school-types.tsv

ADDRESS_DATA=\
	data/discovery/address/addresses.tsv\
	data/discovery/street/streets.tsv

MAPS=\
	maps/addresses.tsv\
	maps/religious-character.tsv\
	maps/diocese.tsv\
	maps/school-gender.tsv\
	maps/school-phase.tsv\
	maps/school-type.tsv

all:: flake8 $(DATA)

data/alpha/school-eng/schools.tsv: mix.deps data/discovery/school-eng/schools.tsv
	@mkdir -p data/alpha/school-eng
	[[ -e $@ ]] || csvgrep -tc school-authority -m "919" < data/discovery/school-eng/schools.tsv | csvformat -T > $@

data/discovery/school-eng/schools.tsv: bin/schools.py cache/edubase.csv $(MAPS) $(SCHOOL_DATA)
	@mkdir -p data/discovery/school-eng
	[[ -e $@ ]] || csvgrep -c 'GOR (name)' -im 'Wales' < cache/edubase.csv | bin/schools.py > $@

data/discovery/school-wls/schools.tsv:
	@mkdir -p data/discovery/school-wls
	[[ -e $@ ]] || csvgrep -c 'GOR (name)' -m 'Wales' < cache/edubase.csv | bin/schools.py > $@

data/alpha/school-trust/school-trusts.tsv: cache/links mix.deps
	@mkdir -p data/alpha/school-trust
	[[ -e $@ ]] || mix run -e 'SchoolTrust.trust_tsv' > data/alpha/school-trust/tmp.tsv
	[[ -e $@ ]] || mix run -e 'SchoolTrust.trust_map_tsv' < data/alpha/school-trust/tmp.tsv > maps/school-trust.tsv
	[[ -e $@ ]] || mix run -e 'SchoolTrust.trust_data_tsv' < data/alpha/school-trust/tmp.tsv > $@
	rm -f data/alpha/school-trust/tmp.tsv

mix.deps:
	[[ -e mix.lock ]] || mix deps.get
	mix compile

# extract school addresses from address-data
data/discovery/address/addresses.tsv:	bin/addresses.py data/discovery/school-eng/schools.tsv
	@mkdir -p data/discovery/address
	bin/addresses.py < data/discovery/school-eng/schools.tsv > $@

# extract school streets from address-data
data/discovery/street/streets.tsv:	bin/streets.py data/discovery/address/addresses.tsv maps/locality.tsv
	@mkdir -p data/discovery/street
	bin/streets.py < data/discovery/address/addresses.tsv > $@

# download from EDUBASE
# - contains invalid UTF-8 characters ..
cache/edubase.csv:
	@mkdir -p cache
	curl -s $(EDUBASE_URL) | iconv -f ISO-8859-1 -t UTF-8 > $@

cache/links:
	[[ -e "./cache/links.xhtml?printable=1&urn=402378" ]] || \
	  ( \
		  cd cache && sed 1d edubase.csv | \
		  awk -F "\"*,\"*" '{ print "http://www.education.gov.uk/edubase/establishment/links.xhtml?printable=1&urn="$$1}' | \
			xargs -P4 -n 1 curl -S -O \
		)

init::
	pip3 install -r requirements.txt

flake8:
	flake8 --max-line-length=109 bin

prune::
	rm -rf cache
	rm -rf data/discovery/school

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
