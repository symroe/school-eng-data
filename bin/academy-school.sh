#!/bin/sh

csvcut -tc school-eng,school-type,school-authority-eng data/alpha/school-eng/schools.tsv \
| csvformat -T > ./maps/tmp1.tsv \
&& csvjoin --left -tc school-type maps/tmp1.tsv data/alpha/school-type/school-types.tsv \
| csvformat -T > ./maps/types.tsv \
&& ACADEMY=true UMBRELLA=false bundle exec ruby ./lib/school_trust.rb \
| sed 's/school\([[:blank:]]\)/academy-school\1/'
