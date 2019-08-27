#!/bin/bash

# Sets env vars from input file ("$1"):
while read p; do
	key=${p%=*}
    val=`echo ${p#*=} | sed -e 's/^"\|"$//g' -e 's/\\r//g'`
    export $key=$val
done <"$1"