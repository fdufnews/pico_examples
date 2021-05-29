#!/bin/bash
for file in *.jpg
do
    output=${file%jpg}raw
    echo  "input : "$file
    echo  "output : "$output
    python imgconvert.py $file $output 80 160
done
