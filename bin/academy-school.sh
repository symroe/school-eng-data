#!/bin/sh

csvgrep -c 'TypeOfEstablishment (name)' -f lists/academy-types/types.txt ./cache/edubase.csv \
| csvcut -c URN,'TypeOfEstablishment (name)','Trusts (name)','SchoolSponsors (name)' \
| csvformat -T > tmp1.tsv \
&& csvjoin --left -tc 'TypeOfEstablishment (name)',name tmp1.tsv data/alpha/school-type/school-types.tsv \
| csvcut -c URN,school-type,'Trusts (name)','SchoolSponsors (name)' \
> tmp2.csv \
&& csvjoin --left -c 'Trusts (name)',name tmp2.csv lists/edubase-school-trust/trusts-with-matched-company.csv \
| csvcut -c URN,school-type,company,'SchoolSponsors (name)' \
| csvformat -T \
> tmp3.tsv \
&& csvjoin --left -tc URN,school tmp3.tsv maps/school-to-edubase-school-trust.tsv \
| csvcut -c URN,school-type,company,school-trust-join-date,'SchoolSponsors (name)' \
| sed 's/^URN,school-type,company,school-trust-join-date,SchoolSponsors (name)$/academy-school-eng,school-type,academy-trust,school-trust-join-date,academy-sponsor/' \
| csvformat -T
