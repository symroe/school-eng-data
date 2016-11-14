#!/bin/sh

( echo 'urn,establishment-type,establishment-group-type' && \
  ls cache/establishmentdetails/ \
  | sed 's/est/cache\/establishmentdetails\/est/' \
  | xargs -n 1 cat \
  | grep -e 'URN\|Type Group\|Type of' \
  | sed 's/.*URN \([^<]*\)<.*/\1/' \
  | sed 's/^\([^ ]*\) .*<th style="">Type of Establishment<\/th><td class="underline"><div title="\([^"]*\)".*/\1,\2/' \
  | sed 's/^\([^ ]*\) .*<th style="">Establishment Type Group<\/th><td class="underline"><div title="\([^"]*\)".*/\1,\2|/' \
  | tr -d '\n' \
  | tr '|' '\n' \
) \
| csvformat -T
