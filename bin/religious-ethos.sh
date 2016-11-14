#!/bin/sh

( echo 'urn,religious-ethos' && \
  ls cache/establishmentdetails/ \
  | sed 's/est/cache\/establishmentdetails\/est/' \
  | xargs -n 1 cat \
  | grep -A 3 -e 'URN\|Ethos' \
  | grep -e 'URN\|Diocese' \
  | sed 's/.*URN \([^<]*\)<.*/\1/' \
  | sed 's/^\([^ ]*\) .*<\/noscript><\/th><td class="underline"><div title="\([^"]*\)".*/\1,\2|/' \
  | tr -d '\n' \
  | tr '|' '\n' \
  | sed 's/Does not apply//' \
  | sed 's/None//' \
) \
| csvformat -T
