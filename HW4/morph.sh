#! /bin/bash
while read line

do
  echo -e "$line\n" | python2.7 split_.py | carmel -sli $1

done <$2
