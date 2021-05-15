#!/bin/bash
for file in *.jpg
do
    output=${file%jpg}py
    dict=${file%.jpg}
    echo  "input : "$file
    echo "dict : "$dict
    echo  "output : "$output
    python imgconvert.py $file $dict $output 74 64
done
