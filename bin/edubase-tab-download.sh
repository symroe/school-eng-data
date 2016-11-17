#!/bin/sh

SCHOOL_TAB=$1
echo $SCHOOL_TAB
mkdir -p cache/$SCHOOL_TAB
cd ./cache/$SCHOOL_TAB && \
	sed 1d ../edubase.csv \
	| awk -v tab="$SCHOOL_TAB" -F "\"*,\"*" '{ print "./"tab".xhtml?printable=1&urn="$1}' \
	| xargs -n 1 ls 2>&1 \
	| grep No \
	| awk '{ print $2 }' \
	| tr -d ':' \
	| sed 's/^\.//' \
	| awk -F "\"*,\"*" '{ print "http://www.education.gov.uk/edubase/establishment"$1}' \
	| xargs -P4 -n 1 curl -s -S -O
