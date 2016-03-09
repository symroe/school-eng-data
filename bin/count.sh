#!/bin/sh

csv="$1"
cols="$2"

  csvtool -u TAB namedcol "$cols" "$csv" |
  tail -n +2 |
  sort |
  uniq -c |
  sort -rn |
  sed -e 's/^ *//' -e 's/ /	/'
