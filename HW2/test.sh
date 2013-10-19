#! /bin/bash

while read line

do 
  echo -e "$line\n" | carmel -sli $1

done < $2 


