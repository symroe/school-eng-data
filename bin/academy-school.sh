#!/bin/sh

csvgrep -c 'TypeOfEstablishment (name)' -f lists/academy-types/types.txt ./cache/edubase.csv \
| csvcut -c URN,'TypeOfEstablishment (name)','Trusts (name)','SchoolSponsors (name)' \
| sed 's/Free Schools Special/Special Free School/' \
| sed 's/Free Schools/Free School/' \
| sed 's/Studio Schools/Studio School/' \
| csvformat -T > tmp-edubase-academies.tsv \
&& csvjoin --left -tc 'TypeOfEstablishment (name)',name tmp-edubase-academies.tsv data/alpha/school-type/school-types.tsv \
| csvcut -c URN,school-type,'Trusts (name)','SchoolSponsors (name)' \
> tmp-academies.csv \
&& csvcut -c 'Group Name','Companies House Number' lists/edubase-academy-trust/all-open-sats-and-mats-161122.csv \
| sed 's/,\([0-1]\)/,company:\1/' \
> tmp-edubase-company-numbers.csv \
&& csvjoin --left -c 'Trusts (name)','Group Name' tmp-academies.csv tmp-edubase-company-numbers.csv \
| csvcut -c URN,school-type,'Trusts (name)','Companies House Number','SchoolSponsors (name)' \
| sed 's/Companies House Number/company-no/' \
> tmp-academies-first-company-number.csv \
&& csvjoin --left -c 'Trusts (name)',name tmp-academies-first-company-number.csv lists/edubase-school-trust/trusts-with-matched-company.csv \
| csvcut -c URN,school-type,company-no,company,'SchoolSponsors (name)' \
| csvformat -T \
> tmp-academies-second-company-number.tsv \
&& bundle exec ruby ./bin/company-number.rb \
> tmp-academies-with-company-number.tsv \
&& csvjoin --left -tc URN,school tmp-academies-with-company-number.tsv maps/school-to-edubase-school-trust.tsv \
| csvcut -c URN,school-type,company,school-trust-join-date,'SchoolSponsors (name)' \
| sed 's/^URN,school-type,company,school-trust-join-date,SchoolSponsors (name)$/academy-school-eng,school-type,academy-trust,school-trust-join-date,academy-sponsor/' \
| csvformat -T
