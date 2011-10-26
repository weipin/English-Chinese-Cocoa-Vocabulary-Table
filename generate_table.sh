#!/usr/bin/env bash

./readme2table.py -f README -o table.txt
./txt2csv.py -f table.txt -o table.csv
