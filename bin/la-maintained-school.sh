#!/bin/sh

csvgrep -c 'TypeOfEstablishment (name)' -f lists/la-maintained-types/types.txt ./cache/edubase.csv \
| csvcut -c URN,'TypeOfEstablishment (name)','Trusts (name)','Federations (name)' \
| sed 's/^URN,TypeOfEstablishment (name),Trusts (name),Federations (name)$/la-maintained-school-eng,school-type-name,foundation-trust,school-federation/' \
| csvformat -T \
> tmp.tsv && \
csvjoin -tc school-type-name,name tmp.tsv data/alpha/school-type/school-types.tsv \
| csvcut -c la-maintained-school-eng,school-type,foundation-trust,school-federation \
| csvformat -T
