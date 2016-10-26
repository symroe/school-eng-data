#!/bin/sh

( csvsql -t --query \
  'select e.edubase,e.name,e."local-authority" from edubase as e where e."local-authority" is NULL' \
  ../local-authority-data/maps/edubase.tsv \
  && \
  csvsql -t --query \
  'select e.edubase,"",e."local-authority" from edubase as e where e."local-authority" like "local-authority-eng%"' \
  ../local-authority-data/maps/edubase.tsv \
) \
| sed 's/edubase,name,local-authority/school-authority,name,organisation/' \
| grep -v edubase \
| csvformat -T
