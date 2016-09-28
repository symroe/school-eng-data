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
	lists/edubase-school-trust-name/trusts.tsv\
	lists/edubase-school-trust/trusts.tsv\
	maps/school-type.tsv

all:: flake8 $(DATA)

data/alpha/school-eng/schools.tsv: mix.deps data/discovery/school-eng/schools.tsv
	@mkdir -p data/alpha/school-eng
	[[ -e $@ ]] || csvgrep -tc school-authority -m "919" < data/discovery/school-eng/schools.tsv | csvformat -T > $@

data/discovery/school-eng/schools.tsv: bin/schools.py cache/edubase.csv $(MAPS) $(SCHOOL_DATA)
	@mkdir -p data/discovery/school-eng
	[[ -e $@ ]] || csvgrep -c 'GOR (name)' -im 'Wales' < cache/edubase.csv | bin/schools.py | sed 's/^school\([[:blank:]]\)/school-eng\1/' > $@

data/discovery/school-wls/schools.tsv:
	@mkdir -p data/discovery/school-wls
	[[ -e $@ ]] || csvgrep -c 'GOR (name)' -m 'Wales' < cache/edubase.csv | bin/schools.py | sed 's/^school\([[:blank:]]\)/school-wls\1/' > $@

data/alpha/school-trust/school-trusts.tsv: mix.deps
	@mkdir -p data/alpha/school-trust
	[[ -e $@ ]] || \
	csvcut -c school-trust,name,company lists/edubase-school-trust/trusts-with-matched-company.csv \
	| sed 's/school-trust,name,company/school-trust,name,organisation/' \
	| mix run -e 'SchoolTrust.final_trust_tsv' \
	> $@

lists/edubase-school-trust/trusts.tsv: lists/edubase-school-trust-name/trusts.tsv
	@mkdir -p lists/edubase-school-trust
	[[ -e $@ ]] || \
	csvjoin --outer -tc name lists/edubase-school-trust-name/trusts.tsv lists/edubase-multi-academy-trust/trusts.tsv \
	| csvcut -c school-trust,name,type,edubase-school-trust,organisation \
	> tmp.csv
	[[ -e $@ ]] || \
	csvjoin --outer -c name tmp.csv lists/edubase-umbrella-trusts/trusts.csv \
	| csvcut -c school-trust,name,type,is-umbrella,edubase-school-trust,organisation \
	| csvformat -T \
	> $@
	rm -f tmp.csv

lists/edubase-multi-academy-trust/trusts.tsv: cache/links mix.deps
	@mkdir -p lists/edubase-multi-academy-trust
	[[ -e $@ ]] || mix run -e 'SchoolTrust.trust_tsv' > maps/tmp.tsv

	[[ -e $@ ]] || csvcut -tc urn,school-trust maps/tmp.tsv \
	| csvsort -c urn \
	| csvformat -T \
	| sed 's/urn\([[:blank:]]\)/school\1/' \
	| sed 's/\([[:blank:]]\)school-trust/\1edubase-school-trust/' \
	> maps/school-to-edubase-school-trust.tsv

	[[ -e $@ ]] || mix run -e 'SchoolTrust.trust_data_tsv' < maps/tmp.tsv > $@
	rm -f maps/tmp.tsv

lists/edubase-school-trust-name/trusts.tsv: lists/edubase-multi-academy-trust/trusts.tsv
	# split two trusts separated by ~ onto separate lines
	# remove duplicate trust names
	# sort by school URN
	# remove school URN
	# remove blank lines
	# add line number
	@mkdir -p lists/edubase-school-trust-name
	csvcut -c URN,"Trusts (name)","TrustSchoolFlag (name)" cache/edubase.csv \
	| sed 's/Supported by a multi-academy trust~Supported by an umbrella trust/multi-academy trust + umbrella trust/' \
	| sed 's/Supported by a single-academy trust~Supported by an umbrella trust/single-academy trust + umbrella trust/' \
	| sed 's/St Hildas Catholic Academy Trust/St Hilda’s Catholic Academy Trust/' \
	| sed 's/Ridings Federation of Academies Trust, The/Ridings’ Federation of Academies Trust, The/' \
	| sed 's/The Helston and Lizard Peninsula Trust~The Helston and Lizard Peninsula Education Trust/The Helston and Lizard Peninsula Education Trust/' \
	| sed 's/The Helston and Lizard Peninsula Trust/The Helston and Lizard Peninsula Education Trust/' \
	| sed 's/South Cheshire Catholic Multi-academy Trust, The~South Cheshire Catholic Multi-Academy Trust/South Cheshire Catholic Multi-academy Trust, The/' \
	| sed 's/created in error-//' \
	| sed 's/^URN,Trusts .*/urn,name,type/' \
	| csvgrep -c name -r "." \
	| sed 's/Supported by a //' \
	| sed 's/^\([^,]*,\)\(".*\)~\(.*"\),\([^,]*\)/\1\2\",\4~\1"\3,\4/g' \
	| sed 's/^\([^,]*,\)\([^"].*\)~\(.*\),\([^,]*\)/\1\2,\4~\1\3,\4/g' \
	| tr '~' $$'\n'   \
	| csvcut -c urn,type,name \
	| tr ' ' '_' \
	| csvsort -c name,urn \
	| csvformat -T    \
	| uniq -f2        \
	| tr '_' ' ' \
	| csvsort -tc urn \
	| csvcut -c name,type \
	| csvgrep -c name -r "." \
	| csvcut -lc name,type \
	| sed 's/^line_number/school-trust/' \
	| csvformat -T    \
	> $@

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
